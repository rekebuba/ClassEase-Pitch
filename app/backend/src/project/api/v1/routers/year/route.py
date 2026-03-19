import uuid
from typing import Any, Dict, List, Sequence

from fastapi import APIRouter, HTTPException
from fastapi.logger import logger
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from starlette import status

from project.api.v1.routers.dependencies import SessionDep, admin_route, shared_route
from project.api.v1.routers.year.schema import (
    DeleteYearSuccess,
    NewYear,
    NewYearSuccess,
    YearSummary,
)
from project.api.v1.routers.year.service import (
    create_academic_term,
    handle_setup_methods,
)
from project.models.grade import Grade
from project.models.subject import Subject
from project.models.year import Year
from project.schema.models import YearWithRelatedSchema
from project.schema.models.grade_schema import GradeNestedSchema
from project.schema.models.subject_schema import SubjectNestedSchema
from project.schema.models.year_schema import YearSchema

router = APIRouter(prefix="/years", tags=["Years"])


@router.get(
    "",
    response_model=List[YearSchema],
)
async def get_years(
    session: SessionDep,
    user_in: shared_route,
) -> Sequence[Year]:
    """
    Returns a list of all academic years in the system.
    """
    years = (await session.execute(select(Year))).scalars().all()

    return years


@router.get(
    "/{year_id}/relation",
    response_model=YearWithRelatedSchema,
)
async def get_year_relation(
    session: SessionDep,
    year_id: uuid.UUID,
    user_in: shared_route,
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
                selectinload(Year.grades),
                selectinload(Year.subjects),
                selectinload(Year.students),
                selectinload(Year.employees),
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
    user_in: shared_route,
    q: str | None = None,
) -> Sequence[Year]:
    """
    Returns a list of all academic years in the system.
    """
    stmt = select(Year)
    if q:
        stmt = stmt.where(Year.name.ilike(f"%{q}%"))
    years = (
        (await session.execute(stmt.order_by(Year.created_at.desc()))).scalars().all()
    )

    return years


@router.get(
    "/{year_id}",
    response_model=YearSchema,
)
async def get_year_by_id(
    session: SessionDep,
    year_id: uuid.UUID,
    user_in: shared_route,
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


@router.post("", response_model=NewYearSuccess, status_code=status.HTTP_201_CREATED)
async def post_year(
    session: SessionDep,
    new_year: NewYear,
    user_in: admin_route,
) -> Dict[str, Any]:
    """
    Creates a new Year
    """
    errors = {}

    existing_year_name = (
        await session.execute(select(Year).where(Year.name == new_year.name))
    ).first()

    if existing_year_name:
        errors["name"] = "Name already exists."

    if errors:
        raise HTTPException(status_code=400, detail=errors)

    try:
        year = Year(
            name=new_year.name,
            calendar_type=new_year.calendar_type,
            status=new_year.status,
            start_date=new_year.start_date,
            end_date=new_year.end_date,
        )
        session.add(year)
        await session.flush()

        create_academic_term(
            year_id=year.id,
            calendar_type=new_year.calendar_type,
            session=session,
        )

        await handle_setup_methods(
            old_year_id=new_year.copy_from_year_id,
            year_id=year.id,
            session=session,
            setup_methods=new_year.setup_methods,
        )

        await session.commit()
        await session.refresh(year)

        return {"message": "Year created Successfully", "id": year.id}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        logger.error(f"Error creating year: {e}")
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Creation failed: {str(e)}")


@router.delete(
    "/{year_id}",
    response_model=DeleteYearSuccess,
)
async def delete_year(
    session: SessionDep,
    year_id: uuid.UUID,
    user_in: admin_route,
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
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")


@router.get(
    "/{year_id}/grades/detail",
    response_model=List[GradeNestedSchema],
)
async def get_detail_grades_by_year_id(
    session: SessionDep,
    year_id: uuid.UUID,
) -> Sequence[Grade]:
    """
    Returns specific academic year
    """
    # TODO: This should be moved to grades route
    year = await session.get(Year, year_id)
    if not year:
        raise HTTPException(
            status_code=404,
            detail=f"Year with ID {year_id} not found.",
        )

    grades = (
        (
            await session.execute(
                select(Grade)
                .where(Grade.year_id == year_id)
                .options(
                    selectinload(Grade.year),
                    selectinload(Grade.sections),
                    selectinload(Grade.streams),
                    selectinload(Grade.students),
                    selectinload(Grade.student_term_records),
                )
            )
        )
        .scalars()
        .all()
    )

    return grades


@router.get(
    "/{year_id}/subjects/detail",
    response_model=List[SubjectNestedSchema],
)
async def get_detail_subjects_by_year_id(
    session: SessionDep,
    year_id: uuid.UUID,
) -> Sequence[Subject]:
    """
    Returns specific academic year
    """
    # TODO: This should be moved to subjects route
    year = await session.get(Year, year_id)
    if not year:
        raise HTTPException(
            status_code=404,
            detail=f"Year with ID {year_id} not found.",
        )

    subjects = (
        (
            await session.execute(
                select(Subject)
                .where(Subject.year_id == year_id)
                .options(
                    selectinload(Subject.teachers),
                    selectinload(Subject.students),
                    selectinload(Subject.mark_lists),
                )
            )
        )
        .scalars()
        .all()
    )

    return subjects
