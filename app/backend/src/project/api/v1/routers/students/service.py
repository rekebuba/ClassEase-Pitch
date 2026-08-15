import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from project.models import (
    ClassSection,
    EnrollmentApplication,
    EnrollmentOpportunity,
    Section,
    Student,
    StudentAcademicBackground,
    StudentAddress,
    StudentHealthRecord,
    User,
    UserGuardian,
)
from project.utils.enum import (
    EnrollmentApplicationStatusEnum,
    StudentApplicationStatusEnum,
)


async def fetch_and_validate_application(
    session: AsyncSession,
    application_id: uuid.UUID,
    acting_school_id: uuid.UUID,
) -> EnrollmentApplication:
    """Fetches the application and ensures it exists, belongs to the school, and isn't already processed."""
    application = await session.scalar(
        select(EnrollmentApplication)
        .options(
            selectinload(EnrollmentApplication.opportunity),
            selectinload(EnrollmentApplication.health_record),
            selectinload(EnrollmentApplication.academic_background),
            selectinload(EnrollmentApplication.address),
        )
        .where(EnrollmentApplication.id == application_id)
    )

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enrollment Application with ID {application_id} not found.",
        )

    if application.school_id != acting_school_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to approve applications for this school.",
        )

    if application.status == EnrollmentApplicationStatusEnum.ACCEPTED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This application has already been approved.",
        )

    return application


async def fetch_class_section(
    session: AsyncSession,
    opportunity: EnrollmentOpportunity,
    section_id: uuid.UUID,
) -> ClassSection:
    """Validates section existence and fetches matching ClassSection for the opportunity."""
    section = await session.scalar(select(Section).where(Section.id == section_id))
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Section with ID {section_id} not found.",
        )

    class_section = await session.scalar(
        select(ClassSection).where(
            ClassSection.academic_year_id == opportunity.academic_year_id,
            ClassSection.grade_stream_id == opportunity.grade_stream_id,
            ClassSection.section_id == section.id,
        )
    )
    if not class_section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class Section for the given year, grade stream, and section not found.",
        )

    return class_section


async def create_student_profile_and_extensions(
    session: AsyncSession,
    application: EnrollmentApplication,
) -> Student:
    """Activates the user account, creates the Student record, and copies 1:1 staging records."""
    # Activate User account if dormant
    student_user = await session.scalar(select(User).where(User.id == application.student_user_id))
    if student_user and not student_user.is_active:
        student_user.is_active = True

    # Create Core Student Profile
    student = Student(
        school_id=application.school_id,
        user_id=application.student_user_id,
        status=StudentApplicationStatusEnum.ACTIVE,
    )
    session.add(student)
    await session.flush()

    # Promote Staging Records -> Active Extensions
    if application.health_record:
        session.add(
            StudentHealthRecord(
                student_id=student.id,
                school_id=application.school_id,
                blood_type=application.health_record.blood_type,
                has_disability=application.health_record.has_disability,
                disability_details=application.health_record.disability_details,
                has_medical_condition=application.health_record.has_medical_condition,
                medical_details=application.health_record.medical_details,
            )
        )

    if application.academic_background:
        session.add(
            StudentAcademicBackground(
                student_id=student.id,
                school_id=application.school_id,
                previous_school=application.academic_background.previous_school,
                is_transfer=application.academic_background.is_transfer,
            )
        )

    if application.address:
        session.add(
            StudentAddress(
                student_id=student.id,
                school_id=application.school_id,
                city=application.address.city,
                state=application.address.state,
                postal_code=application.address.postal_code,
                nationality=application.address.nationality,
                transportation=application.address.transportation,
            )
        )

    return student


async def link_parent_to_student(
    session: AsyncSession,
    *,
    guardian_user_id: uuid.UUID,
    dependent_user_id: uuid.UUID,
    relation: str = "",
) -> None:
    """
    Creates a global link between a parent user and a student user.
    """
    existing = await session.scalar(
        select(UserGuardian).where(
            UserGuardian.guardian_user_id == guardian_user_id,
            UserGuardian.dependent_user_id == dependent_user_id,
        )
    )

    if not existing:
        session.add(
            UserGuardian(
                guardian_user_id=guardian_user_id,
                dependent_user_id=dependent_user_id,
                relation=relation,
            )
        )
        await session.flush()
