import uuid
from typing import List, Sequence

from fastapi import APIRouter, HTTPException
from fastapi.logger import logger
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from starlette import status

from project.api.v1.routers.dependencies import (
    AuthenticatedRoute,
    SessionDep,
    SystemSessionDep,
)
from project.api.v1.routers.year.schema import (
    DeleteYearSuccess,
    NewYear,
    YearSummary,
)
from project.api.v1.routers.year.service import create_academic_term
from project.models.year import Year
from project.schema.models import YearWithRelatedSchema
from project.schema.models.year_schema import YearSchema
from project.schema.schema import SuccessResponse
from project.services.school_provisioning import (
    SchoolProvisioningService,
)
from project.utils.enum import PermissionEnum, RoleEnum

router = APIRouter(prefix="/years", tags=["Years"])


@router.post("", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def post_year(
    session: SessionDep,
    system_session: SystemSessionDep,
    new_year: NewYear,
    user_in: AuthenticatedRoute,
) -> SuccessResponse:
    """
    Creates a new School Year
    """
    if not user_in.has_role(RoleEnum.ADMIN) and not user_in.has_permission(PermissionEnum.YEARS_WRITE):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    errors = {}

    existing_year_name = (
        await session.execute(
            select(Year).where(
                Year.name == new_year.name,
            )
        )
    ).first()

    if existing_year_name:
        errors["name"] = "Name already exists."

    if errors:
        raise HTTPException(status_code=400, detail=errors)

    try:
        year = Year(
            school_id=user_in.membership.school_id,
            name=new_year.name,
            calendar_type=new_year.calendar_type,
            status=new_year.status,
            start_date=new_year.start_date,
            end_date=new_year.end_date,
        )
        session.add(year)
        await session.flush()

        if new_year.setup_methods == "Default Template":
            # Populate the explicit year with the default blueprint structure.
            await SchoolProvisioningService.setup_academic_year_from_blueprint(
                tenant_session=session,
                system_session=system_session,
                school_id=user_in.membership.school_id,
                year_id=year.id,
            )
        elif new_year.setup_methods == "Last Year Copy":
            try:
                await SchoolProvisioningService.setup_academic_year_from_previous_year(
                    tenant_session=session,
                    school_id=user_in.membership.school_id,
                    year_id=year.id,
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"setupMethods": str(e)},
                )
        elif new_year.setup_methods == "Manual":
            create_academic_term(
                year_id=year.id,
                school_id=user_in.membership.school_id,
                calendar_type=new_year.calendar_type,
                session=session,
            )

        await session.commit()

        return SuccessResponse(message="Year created Successfully", id=year.id)
    except HTTPException:
        await session.rollback()
        raise
    except Exception as e:
        logger.error(f"Error creating year: {e}")
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Creation failed: {str(e)}")


@router.get(
    "",
    response_model=List[YearSchema],
)
async def get_years(
    session: SessionDep,
    user_in: AuthenticatedRoute,
) -> Sequence[Year]:
    """
    Returns a list of all academic years in the system.
    """
    if not user_in.has_permission(PermissionEnum.YEARS_READ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to read academic years.",
        )

    years = (await session.execute(select(Year).order_by(Year.created_at.desc()))).scalars().all()

    return years


@router.get(
    "/{year_id}/relation",
    response_model=YearWithRelatedSchema,
)
async def get_year_relation(
    session: SessionDep,
    year_id: uuid.UUID,
    user_in: AuthenticatedRoute,
) -> Year:
    """
    Returns a specific academic year with all its relationship.
    """
    year = (
        await session.execute(
            select(Year)
            .where(Year.id == year_id)
            .options(
                selectinload(Year.events),
                selectinload(Year.academic_terms),
            )
        )
    ).scalar_one_or_none()

    if not year:
        raise HTTPException(
            status_code=404,
            detail=f"Year with ID {year_id} not found.",
        )

    return year


@router.get(
    "/summary",
    response_model=List[YearSummary],
)
async def get_year_summary(
    session: SessionDep,
    user_in: AuthenticatedRoute,
    q: str | None = None,
) -> Sequence[Year]:
    """
    Returns a list of all academic years in the system.
    """
    stmt = select(Year)
    if q:
        stmt = stmt.where(Year.name.ilike(f"%{q}%"))
    years = (await session.execute(stmt.order_by(Year.created_at.desc()))).scalars().all()

    return years


@router.get(
    "/{year_id}",
    response_model=YearSchema,
)
async def get_year_by_id(
    session: SessionDep,
    year_id: uuid.UUID,
    user_in: AuthenticatedRoute,
) -> Year:
    """
    Returns specific academic year
    """
    year = await session.get(Year, year_id)
    if not year:
        raise HTTPException(
            status_code=404,
            detail=f"Year with ID {year_id} not found.",
        )

    return year


@router.delete(
    "/{year_id}",
    response_model=DeleteYearSuccess,
)
async def delete_year(
    session: SessionDep,
    year_id: uuid.UUID,
    user_in: AuthenticatedRoute,
) -> DeleteYearSuccess:
    """
    Deletes an existing academic year in the system.
    """
    year = await session.get(Year, year_id)
    if not year:
        raise HTTPException(
            status_code=404,
            detail=f"Year with ID {year_id} not found.",
        )

    try:
        session.delete(year)
        await session.commit()

        return DeleteYearSuccess(message="Year deleted successfully")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")
