#!/usr/bin/python3
"""Public views module for the API"""

from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from starlette import status

from api.v1.routers.dependencies import SessionDep
from api.v1.routers.registrations.schema import (
    RegistrationResponse,
    RegistrationStep,
    StudentRegistrationForm,
    StudRegStep1,
    StudRegStep2,
    StudRegStep3,
    StudRegStep4,
    StudRegStep5,
)
from models.admin import Admin
from models.grade import Grade
from models.student import Student
from models.subject import Subject
from models.teacher import Teacher
from schema.models.admin_schema import AdminSchema
from schema.models.grade_schema import GradeSchema
from schema.models.subject_schema import SubjectSchema
from schema.models.teacher_schema import TeacherWithRelatedSchema

router = APIRouter(prefix="/register", tags=["registration"])


@router.post("/admins", response_model=RegistrationResponse)
def register_new_admin(
    session: SessionDep, admin_data: AdminSchema
) -> RegistrationResponse:
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

    return RegistrationResponse(
        id=new_admin.id, message="Admin Registered Successfully"
    )


@router.post("/students/step1", response_model=RegistrationStep)
def register_student_step1(
    session: SessionDep, student_data: StudRegStep1
) -> RegistrationStep:
    """Validate student data for each step"""
    return RegistrationStep(message="Student Step 1 Successful")


@router.post("/students/step2", response_model=RegistrationStep)
def register_student_step2(
    session: SessionDep, student_data: StudRegStep2
) -> RegistrationStep:
    """Validate student data for each step"""
    return RegistrationStep(message="Student Step 2 Successful")


@router.post("/students/step3", response_model=RegistrationStep)
def register_student_step3(
    session: SessionDep, student_data: StudRegStep3
) -> RegistrationStep:
    """Validate student data for each step"""
    return RegistrationStep(message="Student Step 3 Successful")


@router.post("/students/step4", response_model=RegistrationStep)
def register_student_step4(
    session: SessionDep, student_data: StudRegStep4
) -> RegistrationStep:
    """Validate student data for each step"""
    return RegistrationStep(message="Student Step 4 Successful")


@router.post("/students/step5", response_model=RegistrationStep)
def register_student_step5(
    session: SessionDep, student_data: StudRegStep5
) -> RegistrationStep:
    """Validate student data for each step"""
    return RegistrationStep(message="Student Step 5 Successful")


@router.post("/students", status_code=201, response_model=RegistrationResponse)
def register_new_student(
    session: SessionDep,
    student_data: StudentRegistrationForm,
) -> RegistrationResponse:
    """Registers a new student in the system."""
    grade = session.get(Grade, student_data.registered_for_grade_id)
    if not grade:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid grade"
        )

    # Convert to dictionary before unpacking
    student_dict = student_data.model_dump(exclude_none=True)

    # Create SQLAlchemy model instance
    new_student = Student(**student_dict)

    session.add(new_student)
    session.commit()

    return RegistrationResponse(
        id=new_student.id, message="Student Registered Successfully"
    )


@router.post("/teachers", response_model=RegistrationResponse)
def register_new_teacher(
    session: SessionDep,
    teacher_data: TeacherWithRelatedSchema,
) -> RegistrationResponse:
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

    return RegistrationResponse(
        id=new_teacher.id, message="Teacher Registered Successfully"
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
