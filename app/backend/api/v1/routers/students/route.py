import uuid
from typing import Annotated, List, Sequence

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select

from api.v1.routers.dependencies import SessionDep, admin_route
from api.v1.routers.schema import FilterParams
from api.v1.routers.students.schema import StudentBasicInfo
from models.grade import Grade
from models.student import Student
from models.year import Year
from schema.schema import SuccessResponseSchema

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


@router.delete("/{student_id}", response_model=SuccessResponseSchema)
def delete_student(
    session: SessionDep,
    student_id: uuid.UUID,
    user_in: admin_route,
) -> SuccessResponseSchema:
    """This endpoint will delete students based on the provided IDs."""
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found.",
        )
    session.delete(student)
    session.commit()
    return SuccessResponseSchema(message="Student deleted successfully.")
