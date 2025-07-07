#!/usr/bin/python3
"""Public views module for the API"""

from flask import Response, request, jsonify
from pydantic import TypeAdapter, ValidationError
from typing import List, Tuple

from sqlalchemy import select
from sqlmodel import col

from api.v1.views.shared import auths as auth
from api.v1.views.methods import parse_nested_form
from api.v1.views.shared.registration.methods import create_role_based_user
from api.v1.views.shared.registration.schema import (
    DumpResultSchema,
    StudentRegistrationSchema,
    TeacherRegistrationSchema,
)
from extension.enums.enum import RoleEnum
from extension.pydantic.models.subject_schema import SubjectSchema
from extension.pydantic.models.teacher_schema import (
    TeacherRelationshipSchema,
    TeacherSchema,
)

from models import storage
from api.v1.views import errors
from models.grade import Grade
from models.student import Student
from models.subject import Subject
from models.teacher import Teacher
from sqlalchemy.exc import SQLAlchemyError

from models.year import Year


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


@auth.route("/register/student", methods=["POST"])
def register_new_student() -> Tuple[Response, int]:
    """Registers a new student in the system."""

    try:
        data = request.get_json()
        grade_id = storage.session.scalar(
            select(Grade.id).where(Grade.grade == data.get("starting_grade"))
        )
        if not grade_id:
            raise ValueError("Invalid grade provided. Please check your input.")
        data["starting_grade_id"] = grade_id

        # Validate and parse the incoming JSON
        student_data = StudentRegistrationSchema.model_validate(data)

        # Convert to dictionary before unpacking
        student_dict = student_data.model_dump(exclude={"starting_grade"})

        # Create SQLAlchemy model instance
        new_student = Student(**student_dict)

        storage.session.add(new_student)
        storage.session.commit()

        return jsonify(message="student registered successfully!"), 201
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
        teacher_data = TeacherRegistrationSchema.model_validate_json(request.data)

        # Start transaction
        subjects = storage.session.scalars(
            select(Subject).where(Subject.name.in_(teacher_data.subjects_to_teach))
        ).all()
        grades = storage.session.scalars(
            select(Grade).where(Grade.grade.in_(teacher_data.grade_to_teach))
        ).all()

        # Validate all subjects/grades exist
        _validate_relations(
            requested_subjects=teacher_data.subjects_to_teach,
            found_subjects=list(subjects),
            requested_grades=teacher_data.grade_to_teach,
            found_grades=list(grades),
        )

        # Convert to dictionary before unpacking
        teacher_dict = teacher_data.model_dump(
            exclude={"grade_to_teach", "subjects_to_teach"},
            exclude_unset=True,
        )

        # Create SQLAlchemy model instance
        new_teacher = Teacher(**teacher_dict)

        # Add relationships after creation
        new_teacher.subjects_to_teach = list(subjects)
        new_teacher.grade_to_teach = list(grades)

        storage.session.add(new_teacher)
        storage.session.commit()

        return jsonify(message="teacher registered successfully!"), 201
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
    requested_subjects: List[str],
    found_subjects: List[Subject],
    requested_grades: List[str],
    found_grades: List[Grade],
) -> None:
    """Validate that all requested relations exist."""
    missing_subjects = set(requested_subjects) - {s.name for s in found_subjects}
    missing_grades = set(requested_grades) - {g.grade for g in found_grades}

    errors = []
    if missing_subjects:
        errors.append(f"Invalid subjects: {', '.join(missing_subjects)}")
    if missing_grades:
        errors.append(f"Invalid grade: {', '.join(missing_grades)}")

    if errors:
        raise ValueError(" | ".join(errors))
