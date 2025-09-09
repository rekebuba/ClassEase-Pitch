#!/usr/bin/python3
"""Public views module for the API"""

from typing import List

from fastapi import APIRouter
from sqlalchemy import select

from api.v1.routers.dependencies import SessionDep
from api.v1.routers.registrations.schema import RegistrationResponse
from extension.pydantic.models.admin_schema import AdminSchema
from extension.pydantic.models.grade_schema import GradeSchema
from extension.pydantic.models.student_schema import StudentWithRelatedSchema
from extension.pydantic.models.subject_schema import SubjectSchema
from extension.pydantic.models.teacher_schema import TeacherWithRelatedSchema
from extension.pydantic.response.schema import SuccessResponseSchema
from models.admin import Admin
from models.grade import Grade
from models.student import Student
from models.subject import Subject
from models.teacher import Teacher

router = APIRouter(prefix="/register", tags=["registration"])


@router.post(
    "/admins", response_model=SuccessResponseSchema[RegistrationResponse, None, None]
)
def register_new_admin(
    session: SessionDep, admin_data: AdminSchema
) -> SuccessResponseSchema[RegistrationResponse, None, None]:
    """Registers a new admin in the system."""

    # Create SQLAlchemy model instance
    new_admin = Admin(
        first_name=admin_data.first_name,
        father_name=admin_data.father_name,
        grand_father_name=admin_data.grand_father_name,
        date_of_birth=admin_data.date_of_birth,
        gender=admin_data.gender,
        email=admin_data.email,
        phone=admin_data.phone,
        address=admin_data.address,
    )

    session.add(new_admin)
    session.commit()

    return SuccessResponseSchema(
        data=RegistrationResponse(id=new_admin.id),
        message="Admin Registered Successfully",
    )


@router.post(
    "/students", response_model=SuccessResponseSchema[RegistrationResponse, None, None]
)
def register_new_student(
    session: SessionDep,
    student_data: StudentWithRelatedSchema,
) -> SuccessResponseSchema[RegistrationResponse, None, None]:
    """Registers a new student in the system."""

    # grades = session.scalar(
    #     select(Grade).where(Grade.id == student_data.starting_grade_id)
    # )

    # if not grades:
    #     raise ValueError(
    #         f"Invalid starting grade {student_data.starting_grade_id} provided."
    #     )

    # Convert to dictionary before unpacking
    student_dict = student_data.model_dump(exclude_none=True)

    # Create SQLAlchemy model instance
    new_student = Student(**student_dict)

    session.add(new_student)
    session.commit()

    return SuccessResponseSchema(
        data=RegistrationResponse(id=new_student.id),
        message="Student Registered Successfully",
    )


@router.post(
    "/teachers", response_model=SuccessResponseSchema[RegistrationResponse, None, None]
)
def register_new_teacher(
    session: SessionDep,
    teacher_data: TeacherWithRelatedSchema,
) -> SuccessResponseSchema[RegistrationResponse, None, None]:
    """
    Registers a new user (Admin, Student, Teacher) in the system.
    """

    subjects = session.scalars(
        select(Subject).where(
            Subject.id.in_([subject.id for subject in teacher_data.subjects or []])
        )
    ).all()
    grades = session.scalars(
        select(Grade).where(
            Grade.id.in_([grade.id for grade in teacher_data.grades or []])
        )
    ).all()
    subject_schemas = [SubjectSchema.model_validate(subject) for subject in subjects]
    grade_schemas = [GradeSchema.model_validate(grade) for grade in grades]

    if not subject_schemas or not grade_schemas:
        raise ValueError("No valid subjects or grades found for the teacher.")

    # Validate all subjects/grades exist
    _validate_relations(
        requested_subjects=teacher_data.subjects,
        found_subjects=subject_schemas,
        requested_grades=teacher_data.grades,
        found_grades=grade_schemas,
    )

    # Convert to dictionary before unpacking
    teacher_dict = teacher_data.model_dump(
        exclude={
            "grades",
            "subjects",
        },
        exclude_none=True,
    )

    # Create SQLAlchemy model instance
    new_teacher = Teacher(**teacher_dict)

    session.add(new_teacher)

    # Add relationships after creation
    new_teacher.subjects = list(subjects)
    new_teacher.grades = list(grades)

    session.commit()

    return SuccessResponseSchema(
        data=RegistrationResponse(id=new_teacher.id),
        message="Teacher Registered Successfully",
    )


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
