from typing import Annotated, Sequence

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select

from project.api.v1.routers.departments.schema import DepartmentBase
from project.api.v1.routers.dependencies import AuthenticatedRoute, SessionDep
from project.api.v1.routers.schema import SearchParams
from project.models import Department, Employee
from project.schema.models import DepartmentSchema
from project.schema.schema import SuccessResponse
from project.utils.enum import PermissionEnum

router = APIRouter()


@router.post(
    "/departments",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse,
    tags=["Departments"],
)
async def post_department(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    department_data: DepartmentBase,
) -> SuccessResponse:
    """Registers a new department in the system."""
    if not user_in.has_permission(PermissionEnum.EMPLOYEES_WRITE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    if department_data.head_employee_id:
        # Check if the head employee exists and belongs to the same school
        head_employee = await session.get(Employee, department_data.head_employee_id)

        if not head_employee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Head employee does not exist or does not belong to the same school.",
            )

    department = Department(
        school_id=user_in.membership.school_id,
        name=department_data.name,
        code=department_data.code,
        head_employee_id=department_data.head_employee_id,
    )

    session.add(department)
    await session.commit()

    return SuccessResponse(id=department.id, message="Department registered successfully")


@router.get(
    "/departments",
    response_model=list[DepartmentSchema],
    tags=["Departments"],
)
async def get_departments(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    query: Annotated[SearchParams, Query()],
) -> Sequence[Department]:
    """Retrieves all departments in the system."""
    if not user_in.has_permission(PermissionEnum.EMPLOYEES_READ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )
    statement = select(Department)

    if query.q:
        statement = statement.where(Department.name.ilike(f"%{query.q}%"))

    result = await session.execute(statement)
    return result.scalars().all()


@router.get(
    "/departments/{department_id}",
    response_model=DepartmentSchema,
    tags=["Departments"],
)
async def get_department(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    department_id: str,
) -> Department:
    """Retrieves a specific department by its ID."""
    if not user_in.has_permission(PermissionEnum.EMPLOYEES_READ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    department = await session.get(Department, department_id)

    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found.",
        )

    return department
