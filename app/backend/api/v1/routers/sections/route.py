import uuid
from typing import Annotated, List, Sequence

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select

from api.v1.routers.dependencies import SessionDep, shared_route
from api.v1.routers.sections.schema import SectionFilterParams
from models.grade import Grade
from models.section import Section
from schema.models.section_schema import SectionSchema

router = APIRouter(prefix="/sections", tags=["Sections"])


@router.get(
    "/",
    response_model=List[SectionSchema],
)
def get_sections(
    session: SessionDep,
    query: Annotated[SectionFilterParams, Query()],
    user_in: shared_route,
) -> Sequence[Section]:
    """
    Returns specific academic grade
    """
    grade = session.get(Grade, query.grade_id)
    if not grade:
        raise HTTPException(
            status_code=404,
            detail=f"Grade with ID {query.grade_id} not found.",
        )

    sections = session.scalars(
        select(Section).where(Section.grade_id == query.grade_id)
    ).all()

    return sections


@router.get(
    "/{section_id}",
    response_model=SectionSchema,
)
def get_section_by_id(
    session: SessionDep,
    section_id: uuid.UUID,
    user_in: shared_route,
) -> Section:
    """
    Returns specific academic section
    """
    section = session.get(Section, section_id)
    if not section:
        raise HTTPException(
            status_code=404,
            detail=f"Section with ID {section_id} not found.",
        )

    return section
