import uuid
from typing import Annotated, List, Sequence

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from project.api.v1.routers.dependencies import AuthenticatedRoute, SessionDep
from project.api.v1.routers.sections.schema import SectionFilterParams
from project.models.grade import Grade
from project.models.section import Section
from project.schema.models import SectionWithRelatedSchema
from project.schema.models.section_schema import SectionSchema
from project.utils.enum import PermissionEnum

router = APIRouter(prefix="/sections", tags=["Sections"])


@router.get(
    "",
    response_model=List[SectionSchema],
)
async def get_sections(
    session: SessionDep,
    query: Annotated[SectionFilterParams, Query()],
    user_in: AuthenticatedRoute,
) -> Sequence[Section]:
    """
    Returns specific academic grade
    """
    if not user_in.has_permission(PermissionEnum.SECTIONS_READ):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to read sections.",
        )

    grade = await session.get(Grade, query.grade_id)
    if not grade:
        raise HTTPException(
            status_code=404,
            detail=f"Grade with ID {query.grade_id} not found.",
        )

    sections = (await session.execute(select(Section).where(Section.grade_id == query.grade_id))).scalars().all()

    return sections


@router.get(
    "/{section_id}",
    response_model=SectionSchema,
)
async def get_section_by_id(
    session: SessionDep,
    section_id: uuid.UUID,
    user_in: AuthenticatedRoute,
) -> Section:
    """
    Returns specific academic section
    """
    section = await session.get(Section, section_id)
    if not section:
        raise HTTPException(
            status_code=404,
            detail=f"Section with ID {section_id} not found.",
        )

    return section


@router.get(
    "/{section_id}/relation",
    response_model=SectionWithRelatedSchema,
)
async def get_section_related(
    session: SessionDep,
    section_id: uuid.UUID,
    user_in: AuthenticatedRoute,
) -> Section:
    """
    Returns specific academic section
    """
    section = (
        await session.execute(
            select(Section)
            .where(Section.id == section_id)
            .options(
                selectinload(Section.grade),
            )
        )
    ).scalar_one_or_none()

    if not section:
        raise HTTPException(
            status_code=404,
            detail=f"Section with ID {section_id} not found.",
        )

    return section
