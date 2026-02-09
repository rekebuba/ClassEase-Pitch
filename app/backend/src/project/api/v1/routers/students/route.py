import uuid
from typing import Annotated, List, Sequence

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select, update

from project.api.v1.routers.dependencies import SessionDep, admin_route
from project.api.v1.routers.schema import FilterParams
from project.api.v1.routers.students.schema import StudentBasicInfo, UpdateStudentStatus
from project.core.security import get_password_hash
from project.models.grade import Grade
from project.models.student import Student
from project.models.user import User
from project.models.year import Year
from project.schema.schema import SuccessResponseSchema
from project.utils.enum import RoleEnum, StudentApplicationStatusEnum
from project.utils.utils import generate_id

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/", response_model=List[StudentBasicInfo])
def get_students(
    session: SessionDep,
    query: Annotated[FilterParams, Query()],
    user_in: admin_route,
) -> Sequence[Student]:
    """This endpoint will return students based on the provided filters."""
    year = session.get(Year, query.year_id)
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

    students = session.scalars(stm).all()

    return students


@router.get("/{student_id}", response_model=StudentBasicInfo)
def get_student(
    session: SessionDep,
    student_id: uuid.UUID,
    user_in: admin_route,
) -> Student:
    """This endpoint will return a student based on the provided ID."""
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found.",
        )
    return student


@router.delete("/", response_model=SuccessResponseSchema)
def delete_students(
    session: SessionDep,
    student_ids: Annotated[List[uuid.UUID], Query()],
    user_in: admin_route,
) -> SuccessResponseSchema:
    """This endpoint will delete students based on the provided IDs."""
    for student_id in student_ids:
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(
                status_code=404,
                detail=f"Student with ID {student_id} not found.",
            )
        session.delete(student)
    session.commit()
    return SuccessResponseSchema(message="Students deleted successfully.")


@router.patch("/status", response_model=SuccessResponseSchema)
def update_student_status(
    session: SessionDep,
    students: UpdateStudentStatus,
    user_in: admin_route,
) -> SuccessResponseSchema:
    """This endpoint will patch students based on the provided IDs."""
    year = (
        session.query(Year)
        .join(Grade, Grade.year_id == Year.id)
        .join(Student, Student.registered_for_grade_id == Grade.id)
        .first()
    )
    if not year:
        raise HTTPException(
            status_code=404,
            detail="No academic year found for the students.",
        )

    for student_id in students.student_ids:
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(
                status_code=404,
                detail=f"Student with ID {student_id} not found.",
            )

        stmt = (
            update(Student)
            .where(Student.id == student_id)
            .values(status=students.status)
        )

        if (
            students.status == StudentApplicationStatusEnum.ACTIVE
            and student.user_id is None
        ):
            username = generate_id(session=session, role=RoleEnum.STUDENT, year=year)
            new_user = User(
                role=RoleEnum.STUDENT,
                username=generate_id(session=session, role=RoleEnum.STUDENT, year=year),
                password=get_password_hash(username),
            )
            session.add(new_user)
            session.commit()

            stmt.values(user_id=new_user.id)

    session.execute(stmt)
    session.commit()

    return SuccessResponseSchema(
        message=f"Student{'s' if len(students.student_ids) > 1 else ''} Status \
            Updated successfully."
    )
