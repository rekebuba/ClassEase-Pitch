import uuid
from typing import Annotated, List, Sequence

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from project.api.v1.routers.dependencies import (
    AuthenticatedRoute,
    SessionDep,
)
from project.api.v1.routers.teachers.schema import (
    AssignTeacher,
    CreateTeacherProfile,
    TeacherBasicInfo,
    TeacherProfileUpdate,
    TeachersQuery,
)
from project.models import SchoolMembership
from project.models.class_section import ClassSection
from project.models.employee import Employee
from project.models.subject import Subject
from project.models.teacher_profile import TeacherProfile
from project.models.teacher_subject import TeacherSubject
from project.models.teaching_assignment import TeachingAssignment
from project.models.year import Year
from project.schema.schema import SuccessResponse, SuccessResponseSchema
from project.utils.enum import PermissionEnum

router = APIRouter()


@router.get("/teachers", response_model=List[TeacherBasicInfo])
async def get_teachers(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    q: Annotated[TeachersQuery, Query()],
) -> Sequence[TeacherBasicInfo]:
    school_id = user_in.membership.school_id
    stmt = (
        select(TeacherProfile)
        .where(TeacherProfile.school_id == school_id)
        .options(
            selectinload(TeacherProfile.employee).selectinload(Employee.membership).selectinload(SchoolMembership.user),
            selectinload(TeacherProfile.teacher_subjects),
        )
    )

    if q.q:
        stmt = stmt.join(Employee, TeacherProfile.employee_id == Employee.id).where(
            Employee.employee_number.ilike(f"%{q.q}%")
        )

    if q.academic_year_id:
        stmt = stmt.where(TeacherProfile.teacher_subjects.any(TeacherSubject.academic_year_id == q.academic_year_id))

    profiles = (await session.execute(stmt)).scalars().unique().all()
    response: List[TeacherBasicInfo] = []
    for profile in profiles:
        employee = profile.employee
        user = employee.membership.user if employee and employee.membership else None
        full_name = None
        if user:
            full_name = " ".join([p for p in [user.first_name, user.father_name, user.grand_father_name] if p])
        response.append(
            TeacherBasicInfo(
                teacher_profile_id=profile.id,
                employee_id=employee.id,
                user_id=employee.membership.user_id if employee and employee.membership else None,
                employee_number=employee.employee_number,
                employment_status=employee.employment_status,
                full_name=full_name,
                work_email=employee.work_email,
                specialization=profile.specialization,
                subject_ids=[ts.subject_id for ts in profile.teacher_subjects],
            )
        )
    return response


@router.get("/teachers/{teacher_id}", response_model=TeacherBasicInfo)
async def get_teacher(
    teacher_id: uuid.UUID,
    session: SessionDep,
    user_in: AuthenticatedRoute,
) -> TeacherProfile:
    """Retrieve a single teacher by ID."""
    teacher = await session.get(TeacherProfile, teacher_id)

    if not teacher or teacher.school_id != user_in.membership.school_id:
        raise HTTPException(
            status_code=404,
            detail=f"Teacher with ID {teacher_id} not found.",
        )
    return teacher


@router.post(
    "/teacher-profiles",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse,
)
async def create_teacher_profile(
    session: SessionDep,
    payload: CreateTeacherProfile,
    user_in: AuthenticatedRoute,
) -> SuccessResponse:
    """Creates a TeacherProfile for an existing employee."""
    if not user_in.has_permission(PermissionEnum.EMPLOYEES_WRITE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    school_id = user_in.membership.school_id
    employee = await session.get(Employee, payload.employee_id)
    if not employee or employee.school_id != school_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    existing = (
        await session.execute(
            select(TeacherProfile).where(
                TeacherProfile.school_id == school_id,
                TeacherProfile.employee_id == payload.employee_id,
            )
        )
    ).scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Teacher profile already exists.",
        )

    teacher_profile = TeacherProfile(
        school_id=school_id,
        employee_id=payload.employee_id,
        specialization=payload.specialization,
        teacher_license_number=payload.teacher_license_number,
        certifications=payload.certifications,
        highest_education=payload.highest_education,
        years_of_experience=payload.years_of_experience,
    )

    session.add(teacher_profile)
    await session.commit()

    return SuccessResponse(id=teacher_profile.id, message="Teacher profile created successfully.")


@router.post("/teachers", response_model=SuccessResponseSchema)
async def assign_teacher(
    session: SessionDep,
    assign_data: AssignTeacher,
    user_in: AuthenticatedRoute,
) -> SuccessResponseSchema:
    school_id = user_in.membership.school_id

    teacher_profile = await session.get(TeacherProfile, assign_data.teacher_profile_id)
    if not teacher_profile or teacher_profile.school_id != school_id:
        raise HTTPException(status_code=404, detail="Teacher profile not found.")

    subject = await session.get(Subject, assign_data.subject_id)
    if not subject or subject.school_id != school_id:
        raise HTTPException(status_code=404, detail="Subject not found.")

    class_section = await session.get(ClassSection, assign_data.class_section_id)
    if not class_section or class_section.school_id != school_id:
        raise HTTPException(status_code=404, detail="Class section not found.")

    academic_year = await session.get(Year, assign_data.academic_year_id)
    if not academic_year or academic_year.school_id != school_id:
        raise HTTPException(status_code=404, detail="Academic year not found.")

    teacher_subject = (
        await session.execute(
            select(TeacherSubject).where(
                TeacherSubject.school_id == school_id,
                TeacherSubject.teacher_profile_id == assign_data.teacher_profile_id,
                TeacherSubject.subject_id == assign_data.subject_id,
                TeacherSubject.academic_year_id == assign_data.academic_year_id,
            )
        )
    ).scalar_one_or_none()
    if teacher_subject is None:
        teacher_subject = TeacherSubject(
            school_id=school_id,
            teacher_profile_id=assign_data.teacher_profile_id,
            subject_id=assign_data.subject_id,
            academic_year_id=assign_data.academic_year_id,
        )
        session.add(teacher_subject)

    existing_assignment = (
        await session.execute(
            select(TeachingAssignment).where(
                TeachingAssignment.school_id == school_id,
                TeachingAssignment.teacher_profile_id == assign_data.teacher_profile_id,
                TeachingAssignment.subject_offering_id == assign_data.subject_id,
                TeachingAssignment.class_section_id == assign_data.class_section_id,
                TeachingAssignment.academic_year_id == assign_data.academic_year_id,
            )
        )
    ).scalar_one_or_none()
    if existing_assignment:
        raise HTTPException(status_code=400, detail="Assignment already exists.")

    assignment = TeachingAssignment(
        school_id=school_id,
        teacher_profile_id=assign_data.teacher_profile_id,
        subject_offering_id=assign_data.subject_id,
        class_section_id=assign_data.class_section_id,
        academic_year_id=assign_data.academic_year_id,
    )
    session.add(assignment)
    await session.commit()
    return SuccessResponseSchema(message="Teacher assigned successfully.")


@router.patch("/teachers/{teacher_id}", response_model=SuccessResponseSchema)
async def update_teacher(
    teacher_id: uuid.UUID,
    teacher_data: TeacherProfileUpdate,
    session: SessionDep,
    user_in: AuthenticatedRoute,
) -> SuccessResponseSchema:
    """Update a teacher profile."""
    if not user_in.has_permission(PermissionEnum.EMPLOYEES_WRITE):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    teacher = await session.get(TeacherProfile, teacher_id)

    if not teacher or teacher.school_id != user_in.membership.school_id:
        raise HTTPException(
            status_code=404,
            detail=f"Teacher with ID {teacher_id} not found.",
        )

    update_data = teacher_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(teacher, key, value)

    await session.commit()
    return SuccessResponseSchema(message="Teacher updated successfully.")


@router.delete("/teachers/{teacher_id}", response_model=SuccessResponseSchema)
async def delete_teacher(
    teacher_id: uuid.UUID,
    session: SessionDep,
    user_in: AuthenticatedRoute,
) -> SuccessResponseSchema:
    """Delete a teacher profile."""
    if not user_in.has_permission(PermissionEnum.EMPLOYEES_WRITE):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    teacher = await session.get(TeacherProfile, teacher_id)

    if not teacher or teacher.school_id != user_in.membership.school_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Teacher with ID {teacher_id} not found.",
        )

    session.delete(teacher)
    await session.commit()

    return SuccessResponseSchema(message="Teacher deleted successfully.")
