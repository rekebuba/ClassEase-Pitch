import uuid
from typing import Annotated, List, Optional, Sequence

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select

from project.api.v1.routers.dependencies import SessionDep, admin_route
from project.api.v1.routers.employee.schema import (
    EmployeeBasicInfo,
    UpdateEmployeeStatusSchema,
)
from project.core.access_control import provision_user_membership
from project.models.employee import Employee
from project.models.employee_year_link import EmployeeYearLink
from project.models.year import Year
from project.schema.schema import SuccessResponseSchema
from project.utils.enum import (
    EmployeeApplicationStatusEnum,
    EmployeePositionEnum,
    MfaStateEnum,
    RoleEnum,
)
from project.utils.utils import generate_id

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("", response_model=List[EmployeeBasicInfo])
async def get_employees(
    session: SessionDep,
    user_in: admin_route,
    q: Annotated[Optional[str], Query()] = None,
) -> Sequence[Employee]:
    """This endpoint will return employees based on the provided filters."""
    stm = select(Employee)

    if q:
        stm = stm.where(Employee.first_name.ilike(f"%{q}%"))

    employees = (await session.execute(stm)).scalars().all()

    return employees


@router.get("/{employee_id}", response_model=EmployeeBasicInfo)
async def get_employee(
    employee_id: uuid.UUID,
    session: SessionDep,
    user_in: admin_route,
) -> Employee:
    """This endpoint will return a single employee by ID."""
    employee = await session.get(Employee, employee_id)

    if not employee:
        raise HTTPException(
            status_code=404,
            detail=f"Employee with ID {employee_id} not found.",
        )
    return employee


@router.delete("", response_model=SuccessResponseSchema)
async def delete_employees(
    session: SessionDep,
    employee_ids: Annotated[List[uuid.UUID], Query()],
    user_in: admin_route,
) -> SuccessResponseSchema:
    """This endpoint will delete employees by their IDs."""
    for employee_id in employee_ids:
        employee = await session.get(Employee, employee_id)
        if not employee:
            raise HTTPException(
                status_code=404,
                detail=f"Employee with ID {employee_id} not found.",
            )
        session.delete(employee)
    await session.commit()

    return SuccessResponseSchema(message="Employees deleted successfully.")


@router.patch("/status", response_model=SuccessResponseSchema)
async def update_employee_status(
    session: SessionDep,
    employees: UpdateEmployeeStatusSchema,
    user_in: admin_route,
) -> SuccessResponseSchema:
    """This endpoint will update the status of employees by their IDs."""
    year = await session.get(Year, employees.year_id)
    if not year:
        raise HTTPException(
            status_code=404,
            detail="No academic year found.",
        )

    for employee_id in employees.employee_ids:
        employee = await session.get(Employee, employee_id)
        if not employee:
            raise HTTPException(
                status_code=404,
                detail=f"Employee with ID {employee_id} not found.",
            )

        if employee not in year.employees:
            link = EmployeeYearLink(employee_id=employee.id, year_id=year.id)
            session.add(link)

        employee.status = employees.status
        if (
            employees.status == EmployeeApplicationStatusEnum.ACTIVE
            and employee.position == EmployeePositionEnum.TEACHING_STAFF
            and employee.user_id is None
        ):
            username = await generate_id(
                session=session,
                role=RoleEnum.TEACHER,
                year=year,
            )
            new_user, membership = await provision_user_membership(
                session,
                school=user_in.membership.school,
                shell_role=RoleEnum.TEACHER,
                membership_role_name="teacher",
                login_identifier=username,
                password=username,
                email=None,
                phone=None,
                is_active=True,
                is_verified=False,
                mfa_state=MfaStateEnum.VERIFIED,
            )
            employee.user_id = new_user.id
            employee.school_membership_id = membership.id
            employee.school_id = membership.school_id

    await session.commit()
    return SuccessResponseSchema(message="Employees status updated successfully.")
