import uuid
from typing import Annotated, List, Optional, Sequence

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select

from api.v1.routers.dependencies import SessionDep, admin_route
from api.v1.routers.employee.schema import EmployeeBasicInfo, UpdateEmployeeStatusSchema
from models.employee import Employee
from schema.schema import SuccessResponseSchema

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/", response_model=List[EmployeeBasicInfo])
def get_employees(
    session: SessionDep,
    user_in: admin_route,
    q: Annotated[Optional[str], Query()] = None,
) -> Sequence[Employee]:
    """This endpoint will return employees based on the provided filters."""
    stm = select(Employee)

    if q:
        stm = stm.where(Employee.first_name.ilike(f"%{q}%"))

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


@router.patch("/status", response_model=SuccessResponseSchema)
def update_employee_status(
    session: SessionDep,
    employees: UpdateEmployeeStatusSchema,
    user_in: admin_route,
) -> SuccessResponseSchema:
    """This endpoint will update the status of employees by their IDs."""
    for employee_id in employees.employee_ids:
        employee = session.get(Employee, employee_id)
        if not employee:
            raise HTTPException(
                status_code=404,
                detail=f"Employee with ID {employee_id} not found.",
            )
        employee.status = employees.status
    session.commit()
    return SuccessResponseSchema(message="Employees status updated successfully.")
