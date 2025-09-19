import uuid
from typing import Annotated, List, Sequence

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select

from api.v1.routers.dependencies import SessionDep, admin_route
from api.v1.routers.employee.schema import EmployeeBasicInfo
from api.v1.routers.schema import FilterParams
from models import student
from models.employee import Employee
from models.year import Year
from schema.schema import SuccessResponseSchema

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/", response_model=List[EmployeeBasicInfo])
def get_employees(
    session: SessionDep,
    query: Annotated[FilterParams, Query()],
    user_in: admin_route,
) -> Sequence[Employee]:
    """This endpoint will return employees based on the provided filters."""
    year = session.get(Year, query.year_id)
    if not year:
        raise HTTPException(
            status_code=404,
            detail=f"Year with ID {query.year_id} not found.",
        )

    stm = select(Employee)

    if query.q:
        stm = stm.where(Employee.first_name.ilike(f"%{query.q}%"))

    employees = session.scalars(stm).all()

    return employees


@router.get("/{employee_id}", response_model=EmployeeBasicInfo)
def get_employee(
    employee_id: uuid.UUID,
    session: SessionDep,
    user_in: admin_route,
) -> Employee:
    """This endpoint will return a single employee by ID."""
    employee = session.get(Employee, employee_id)
    
    if not employee:
        raise HTTPException(
            status_code=404,
            detail=f"Employee with ID {employee_id} not found.",
        )
    return employee


@router.delete("/", response_model=SuccessResponseSchema)
def delete_employees(
    session: SessionDep,
    employee_ids: Annotated[List[uuid.UUID], Query()],
    user_in: admin_route,
) -> SuccessResponseSchema:
    """This endpoint will delete employees by their IDs."""
    for employee_id in employee_ids:
        employee = session.get(Employee, employee_id)
        if not employee:
            raise HTTPException(
                status_code=404,
                detail=f"Employee with ID {employee_id} not found.",
            )
        session.delete(employee)
    session.commit()

    return SuccessResponseSchema(message="Employees deleted successfully.")
