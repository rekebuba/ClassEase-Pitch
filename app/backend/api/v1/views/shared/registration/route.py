#!/usr/bin/python3
"""Public views module for the API"""

from flask import Response, request, jsonify
from pydantic import ValidationError
from typing import List, Tuple

from sqlalchemy import select

from api.v1.views.shared import auths as auth
from api.v1.views.methods import parse_nested_form
from api.v1.views.shared.registration.methods import create_role_based_user
from api.v1.views.shared.registration.schema import (
    DumpResultSchema,
    SucssussfulRegistrationResponse,
)
from extension.enums.enum import RoleEnum
from extension.pydantic.models.admin_schema import AdminSchema
from extension.pydantic.models.grade_schema import GradeSchema
from extension.pydantic.models.student_schema import StudentWithRelationshipsSchema

from extension.pydantic.models.subject_schema import SubjectSchema
from extension.pydantic.models.teacher_schema import TeacherWithRelationshipsSchema
from models import storage
from api.v1.views import errors
from models.admin import Admin
from models.grade import Grade
from models.student import Student
from models.subject import Subject
from models.teacher import Teacher
from sqlalchemy.exc import SQLAlchemyError


@auth.route("/registration/<role>", methods=["POST"])
def register_new_user(role: str) -> Tuple[Response, int]:
    """
    Registers a new user (Admin, Student, Teacher) in the system.
    """

    try:
        data_to_parse = {**request.form.to_dict(), **request.files.to_dict()}
        data = parse_nested_form(data_to_parse)
        role_enum = RoleEnum.enum_value(role.lower())

        if not data:
            raise Exception("No data provided")

        result = create_role_based_user(role_enum, data)
        if not result:
            raise Exception("Failed to register user")

        validate_data = {
            "message": f"{role} registered successfully!",
            "user": {
                "identification": result.identification,
                "role": result.role,
            },
        }

        schema = DumpResultSchema()
        send_result = schema.dump(validate_data)

        return jsonify(**send_result), 201
    except ValidationError as e:
        storage.rollback()
        return errors.handle_validation_error(e)
    except Exception as e:
        storage.rollback()
        return errors.handle_internal_error(e)


@auth.route("/register/admin", methods=["POST"])
def register_new_admin() -> Tuple[Response, int]:
    """Registers a new admin in the system."""

    try:
        # Validate and parse the incoming JSON
        admin_data = AdminSchema.model_validate_json(request.data)

        # Convert to dictionary before unpacking
        admin_dict = admin_data.model_dump(exclude_none=True)

        # Create SQLAlchemy model instance
        new_admin = Admin(**admin_dict)

        storage.session.add(new_admin)
        storage.session.commit()

        response = SucssussfulRegistrationResponse(
            message="Admin Registered Successfully!",
            id=new_admin.id,
        )

        return jsonify(response.model_dump()), 201
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except SQLAlchemyError as e:
        storage.session.rollback()
        return errors.handle_database_error(e)
    except ValueError as e:
        storage.session.rollback()
        return errors.handle_value_error(e)
    except Exception as e:
        storage.session.rollback()
        return errors.handle_internal_error(e)


@auth.route("/register/student", methods=["POST"])
def register_new_student() -> Tuple[Response, int]:
    """Registers a new student in the system."""

    try:
        # Validate and parse the incoming JSON
        student_data = StudentWithRelationshipsSchema.model_validate_json(request.data)

        grades = storage.session.scalars(
            select(Grade).where(Grade.id == student_data.starting_grade_id)
        ).first()

        if not grades:
            raise ValueError(
                f"Invalid starting grade {student_data.starting_grade_id} provided."
            )

        # Convert to dictionary before unpacking
        student_dict = student_data.model_dump(exclude_none=True)

        # Create SQLAlchemy model instance
        new_student = Student(**student_dict)

        storage.session.add(new_student)
        storage.session.commit()

        response = SucssussfulRegistrationResponse(
            message="Student Registered Successfully!",
            id=new_student.id,
        )

        return jsonify(response.model_dump()), 201
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except SQLAlchemyError as e:
        storage.session.rollback()
        return errors.handle_database_error(e)
    except ValueError as e:
        storage.session.rollback()
        return errors.handle_value_error(e)
    except Exception as e:
        storage.session.rollback()
        return errors.handle_internal_error(e)


@auth.route("/register/teacher", methods=["POST"])
def register_new_teacher() -> Tuple[Response, int]:
    """
    Registers a new user (Admin, Student, Teacher) in the system.
    """
    try:
        # Validate and parse the incoming JSON
        teacher_data = TeacherWithRelationshipsSchema.model_validate_json(request.data)

        subjects = storage.session.scalars(
            select(Subject).where(
                Subject.id.in_(
                    [subject.id for subject in teacher_data.subjects_to_teach or []]
                )
            )
        ).all()
        grades = storage.session.scalars(
            select(Grade).where(
                Grade.id.in_([grade.id for grade in teacher_data.grade_to_teach or []])
            )
        ).all()
        subject_schemas = [
            SubjectSchema.model_validate(subject) for subject in subjects
        ]
        grade_schemas = [GradeSchema.model_validate(grade) for grade in grades]

        if not subject_schemas or not grade_schemas:
            raise ValueError("No valid subjects or grades found for the teacher.")

        # Validate all subjects/grades exist
        _validate_relations(
            requested_subjects=teacher_data.subjects_to_teach,
            found_subjects=subject_schemas,
            requested_grades=teacher_data.grade_to_teach,
            found_grades=grade_schemas,
        )

        # Convert to dictionary before unpacking
        teacher_dict = teacher_data.model_dump(
            exclude={
                "grade_to_teach",
                "subjects_to_teach",
            },
            exclude_none=True,
        )

        # Create SQLAlchemy model instance
        new_teacher = Teacher(**teacher_dict)

        storage.session.add(new_teacher)

        # Add relationships after creation
        new_teacher.subjects_to_teach = list(subjects)
        new_teacher.grade_to_teach = list(grades)

        storage.session.commit()

        response = SucssussfulRegistrationResponse(
            message="Teacher Registered Successfully!",
            id=new_teacher.id,
        )

        return jsonify(response.model_dump()), 201
    except ValidationError as e:
        return errors.handle_validation_error(e)
    except SQLAlchemyError as e:
        storage.session.rollback()
        return errors.handle_database_error(e)
    except ValueError as e:
        storage.session.rollback()
        return errors.handle_value_error(e)
    except Exception as e:
        storage.session.rollback()
        return errors.handle_internal_error(e)


def _validate_relations(
    requested_subjects: List[SubjectSchema] | None,
    found_subjects: List[SubjectSchema],
    requested_grades: List[GradeSchema] | None,
    found_grades: List[GradeSchema],
) -> None:
    if not requested_subjects or not requested_grades:
        raise ValueError("Requested subjects or grades cannot be None or empty.")

    """Validate that all requested relations exist."""
    missing_subjects = {s.name for s in requested_subjects} - {
        s.name for s in found_subjects
    }
    missing_grades = {g.grade for g in requested_grades} - {
        g.grade for g in found_grades
    }

    errors = []
    if missing_subjects:
        errors.append(f"Invalid subjects: {', '.join(missing_subjects)}")
    if missing_grades:
        errors.append(f"Invalid grade: {', '.join(missing_grades)}")

    if errors:
        raise ValueError(" | ".join(errors))
