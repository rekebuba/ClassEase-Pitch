from typing import Annotated, List, Optional, Sequence

from fastapi import APIRouter, Query
from sqlalchemy import select

from api.v1.routers.dependencies import SessionDep, admin_route
from api.v1.routers.teachers.schema import TeacherBasicInfo
from models.employee import Employee
from utils.enum import EmployeePositionEnum

router = APIRouter(prefix="/teachers", tags=["Teachers"])


@router.get("/", response_model=List[TeacherBasicInfo])
def get_teachers(
    session: SessionDep,
    user_in: admin_route,
    q: Annotated[Optional[str], Query()] = None,
) -> Sequence[Employee]:
    """This endpoint will return employees based on the provided filters."""
    stm = select(Employee).where(
        Employee.position == EmployeePositionEnum.TEACHING_STAFF
    )

    if q:
        stm = stm.where(Employee.first_name.ilike(f"%{q}%"))

    employees = session.scalars(stm).all()

    return employees
