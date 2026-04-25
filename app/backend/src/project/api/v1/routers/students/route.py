import uuid
from typing import Annotated, List, Sequence

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select

from project.api.v1.routers.dependencies import SessionDep, admin_route
from project.api.v1.routers.schema import FilterParams
from project.api.v1.routers.students.schema import StudentBasicInfo, UpdateStudentStatus
from project.core.access_control import provision_user_membership
from project.models.grade import Grade
from project.models.student import Student
from project.models.year import Year
from project.schema.schema import SuccessResponseSchema
from project.utils.enum import MfaStateEnum, RoleEnum, StudentApplicationStatusEnum
from project.utils.utils import generate_id

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("", response_model=List[StudentBasicInfo])
async def get_students(
    session: SessionDep,
    query: Annotated[FilterParams, Query()],
    user_in: admin_route,
) -> Sequence[Student]:
    """This endpoint will return students based on the provided filters."""
    year = await session.get(Year, query.year_id)
    if not year:
        raise HTTPException(
            status_code=404,
            detail=f"Year with ID {query.year_id} not found.",
        )

    stm = (
        select(Student)
        .join(Grade, Student.registered_for_grade_id == Grade.id)
        .where(Grade.year_id == query.year_id)
    )

    if query.q:
        stm = stm.where(Student.first_name.ilike(f"%{query.q}%"))

    students = (await session.execute(stm)).scalars().all()

    return students


@router.get("/{student_id}", response_model=StudentBasicInfo)
async def get_student(
    session: SessionDep,
    student_id: uuid.UUID,
    user_in: admin_route,
) -> Student:
    """This endpoint will return a student based on the provided ID."""
    student = await session.get(Student, student_id)
    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found.",
        )
    return student


@router.delete("", response_model=SuccessResponseSchema)
async def delete_students(
    session: SessionDep,
    student_ids: Annotated[List[uuid.UUID], Query()],
    user_in: admin_route,
) -> SuccessResponseSchema:
    """This endpoint will delete students based on the provided IDs."""
    for student_id in student_ids:
        student = await session.get(Student, student_id)
        if not student:
            raise HTTPException(
                status_code=404,
                detail=f"Student with ID {student_id} not found.",
            )
        await session.delete(student)
    await session.commit()
    return SuccessResponseSchema(message="Students deleted successfully.")


@router.patch("/status", response_model=SuccessResponseSchema)
async def update_student_status(
    session: SessionDep,
    students: UpdateStudentStatus,
    user_in: admin_route,
) -> SuccessResponseSchema:
    """This endpoint will patch students based on the provided IDs."""
    for student_id in students.student_ids:
        student = await session.get(Student, student_id)
        if not student:
            raise HTTPException(
                status_code=404,
                detail=f"Student with ID {student_id} not found.",
            )

        student.status = students.status

        if (
            students.status == StudentApplicationStatusEnum.ACTIVE
            and student.user_id is None
        ):
            year = (
                await session.execute(
                    select(Year)
                    .join(Grade, Grade.year_id == Year.id)
                    .where(Grade.id == student.registered_for_grade_id)
                )
            ).scalar_one_or_none()
            if year is None:
                raise HTTPException(
                    status_code=404,
                    detail="No academic year found for the student.",
                )
            username = await generate_id(
                session=session,
                role=RoleEnum.STUDENT,
                year=year,
            )
            new_user, membership = await provision_user_membership(
                session,
                school=user_in.membership.school,
                shell_role=RoleEnum.STUDENT,
                membership_role_name="student",
                login_identifier=username,
                password=username,
                email=None,
                phone=None,
                is_active=True,
                is_verified=False,
                mfa_state=MfaStateEnum.NOT_ENROLLED,
            )
            student.user_id = new_user.id
            student.school_membership_id = membership.id
            student.school_id = membership.school_id

    await session.commit()

    return SuccessResponseSchema(
        message=f"Student{'s' if len(students.student_ids) > 1 else ''} Status \
            Updated successfully."
    )
