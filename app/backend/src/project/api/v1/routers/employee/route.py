import uuid
from typing import Annotated, List, Optional, Sequence

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select

from project.api.v1.routers.dependencies import (
    AuthenticatedRoute,
    SessionDep,
)
from project.api.v1.routers.employee.schema import (
    EmployeePositionCreate,
    EmployeePositionUpdate,
    EmploymentContractCreate,
    PayrollProfileCreate,
    UpdateEmployeeStatusSchema,
)
from project.api.v1.routers.employee.service import EmployeeService
from project.api.v1.routers.school.schema import (
    EmployeeProfile,
)
from project.models import (
    Employee,
    EmployeePosition,
    EmploymentContract,
    PayrollProfile,
    Position,
)
from project.schema.models import EmployeeSchema
from project.schema.schema import SuccessResponse, SuccessResponseSchema
from project.utils.enum import PermissionEnum

router = APIRouter()


@router.post(
    "/employees",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse,
    tags=["Employees"],
)
async def employee(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    employee_data: EmployeeProfile,
) -> SuccessResponse:
    """Registers a new employee in the system."""

    if not user_in.has_permission(PermissionEnum.EMPLOYEES_WRITE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    try:
        employee = await EmployeeService.create_employee_with_membership(
            session=session,
            school_id=user_in.membership.school_id,
            employee_data=employee_data,
        )

        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating employee: {str(e)}",
        )

    return SuccessResponse(id=employee.id, message="employee Registered Successfully")


@router.get("/employees", response_model=List[EmployeeSchema])
async def get_employees(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    q: Annotated[Optional[str], Query()] = None,
) -> Sequence[Employee]:
    """This endpoint will return employees based on the provided filters."""
    stm = select(Employee)

    if q:
        stm = stm.where(Employee.employee_number.ilike(f"%{q}%") | Employee.work_email.ilike(f"%{q}%"))

    employees = (await session.execute(stm)).scalars().all()

    return employees


@router.get("/employees/{employee_id}", response_model=EmployeeSchema)
async def get_employee(
    employee_id: uuid.UUID,
    session: SessionDep,
    user_in: AuthenticatedRoute,
) -> Employee:
    """This endpoint will return a single employee by ID."""
    employee = await session.get(Employee, employee_id)

    if not employee:
        raise HTTPException(
            status_code=404,
            detail=f"Employee with ID {employee_id} not found.",
        )
    return employee


@router.delete("/employees", response_model=SuccessResponseSchema)
async def delete_employees(
    session: SessionDep,
    employee_ids: Annotated[List[uuid.UUID], Query()],
    user_in: AuthenticatedRoute,
) -> SuccessResponseSchema:
    """This endpoint will delete employees by their IDs."""
    for employee_id in employee_ids:
        employee = await session.get(Employee, employee_id)
        if not employee:
            raise HTTPException(
                status_code=404,
                detail=f"Employee with ID {employee_id} not found.",
            )
        await session.delete(employee)
    await session.commit()

    return SuccessResponseSchema(message="Employees deleted successfully.")


@router.patch("/employees/status", response_model=SuccessResponseSchema)
async def update_employee_status(
    session: SessionDep,
    employees: UpdateEmployeeStatusSchema,
    user_in: AuthenticatedRoute,
) -> SuccessResponseSchema:
    """This endpoint will update the status of employees by their IDs."""
    for employee_id in employees.employee_ids:
        employee = await session.get(Employee, employee_id)
        if not employee:
            raise HTTPException(
                status_code=404,
                detail=f"Employee with ID {employee_id} not found.",
            )
        employee.employment_status = employees.status

    await session.commit()
    return SuccessResponseSchema(message="Employees status updated successfully.")


@router.post(
    "/employee-positions",
    tags=["Employee Positions"],
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse,
)
async def create_employee_position(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    position_data: EmployeePositionCreate,
) -> SuccessResponse:
    if not user_in.has_permission(PermissionEnum.EMPLOYEES_WRITE):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    employee = await session.get(Employee, position_data.employee_id)
    if not employee or employee.school_id != user_in.membership.school_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    position = await session.get(Position, position_data.position_id)
    if not position or position.school_id != user_in.membership.school_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Position not found")

    employee_position = EmployeePosition(
        school_id=user_in.membership.school_id,
        employee_id=position_data.employee_id,
        position_id=position_data.position_id,
        start_date=position_data.start_date,
        end_date=position_data.end_date,
        is_primary=position_data.is_primary,
    )

    session.add(employee_position)
    await session.commit()

    return SuccessResponse(id=employee_position.id, message="Employee position assigned successfully")


@router.patch(
    "/employee-positions/{id}",
    tags=["Employee Positions"],
    response_model=SuccessResponseSchema,
)
async def update_employee_position(
    id: uuid.UUID,
    position_data: EmployeePositionUpdate,
    session: SessionDep,
    user_in: AuthenticatedRoute,
) -> SuccessResponseSchema:
    if not user_in.has_permission(PermissionEnum.EMPLOYEES_WRITE):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    employee_position = await session.get(EmployeePosition, id)
    if not employee_position or employee_position.school_id != user_in.membership.school_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee position not found")

    if position_data.end_date is not None:
        employee_position.end_date = position_data.end_date
    if position_data.is_primary is not None:
        employee_position.is_primary = position_data.is_primary

    await session.commit()
    return SuccessResponseSchema(message="Employee position updated successfully")


@router.post(
    "/employment-contracts",
    tags=["Employment Contracts"],
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse,
)
async def create_employment_contract(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    contract_data: EmploymentContractCreate,
) -> SuccessResponse:
    if not user_in.has_permission(PermissionEnum.EMPLOYEES_WRITE):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    employee = await session.get(Employee, contract_data.employee_id)
    if not employee or employee.school_id != user_in.membership.school_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    contract = EmploymentContract(
        school_id=user_in.membership.school_id,
        employee_id=contract_data.employee_id,
        contract_type=contract_data.contract_type,
        hours_per_week=contract_data.hours_per_week,
        start_date=contract_data.start_date,
        end_date=contract_data.end_date,
        status=contract_data.status,
    )

    session.add(contract)
    await session.commit()

    return SuccessResponse(id=contract.id, message="Employment contract created successfully")


@router.post(
    "/payroll-profiles",
    tags=["Payroll Profiles"],
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse,
)
async def create_payroll_profile(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    payroll_data: PayrollProfileCreate,
) -> SuccessResponse:
    if not user_in.has_permission(PermissionEnum.EMPLOYEES_WRITE):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    employee = await session.get(Employee, payroll_data.employee_id)
    if not employee or employee.school_id != user_in.membership.school_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    payroll = PayrollProfile(
        school_id=user_in.membership.school_id,
        employee_id=payroll_data.employee_id,
        bank_name=payroll_data.bank_name,
        bank_account=payroll_data.bank_account,
        tax_identifier=payroll_data.tin_number,
        payment_method=payroll_data.payment_method,
        pay_frequency=payroll_data.pay_frequency,
        base_salary=payroll_data.base_salary,
        currency=payroll_data.currency,
    )

    session.add(payroll)
    await session.commit()

    return SuccessResponse(id=payroll.id, message="Payroll profile created successfully")
