from typing import Sequence

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from project.api.v1.routers.dependencies import AuthenticatedRoute, SessionDep
from project.api.v1.routers.positions.schema import PositionBase
from project.models import Department, Position
from project.schema.models import PositionSchema
from project.schema.schema import SuccessResponse
from project.utils.enum import PermissionEnum

router = APIRouter()


@router.post("/positions", status_code=status.HTTP_201_CREATED, tags=["Positions"])
async def post_position(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    position_data: PositionBase,
) -> SuccessResponse:
    """Registers a new position in the system."""
    if not user_in.has_permission(PermissionEnum.EMPLOYEES_WRITE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    if position_data.department_id:
        # Check if the department exists and belongs to the same school
        department = await session.get(Department, position_data.department_id)

        if not department or department.school_id != user_in.membership.school_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department does not exist or does not belong to the same school.",
            )

    position = Position(
        school_id=user_in.membership.school_id,
        title=position_data.title,
        department_id=position_data.department_id,
    )

    session.add(position)
    await session.commit()

    return SuccessResponse(id=position.id, message="Position registered successfully")


@router.get("/positions", response_model=list[PositionSchema], tags=["Positions"])
async def get_positions(
    session: SessionDep,
    user_in: AuthenticatedRoute,
) -> Sequence[Position]:
    """Retrieves all positions in the system."""
    if not user_in.has_permission(PermissionEnum.EMPLOYEES_READ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )
    statement = select(Position).where(Position.school_id == user_in.membership.school_id)
    result = await session.execute(statement)
    return result.scalars().all()
