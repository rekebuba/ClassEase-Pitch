import uuid
from typing import List, Sequence

from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from api.v1.routers.dependencies import SessionDep
from extension.pydantic.models.section_schema import SectionWithRelatedSchema
from models.grade import Grade
from models.section import Section

router = APIRouter(prefix="/grades/{grade_id}/sections", tags=["Sections"])


@router.get(
    "/",
    response_model=List[SectionWithRelatedSchema],
)
def get_sections(
    session: SessionDep,
    grade_id: uuid.UUID,
) -> Sequence[Section]:
    """
    Returns specific academic grade
    """
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(
            status_code=404,
            detail=f"Grade with ID {grade_id} not found.",
        )

    sections = session.scalars(
        select(Section)
        .where(Section.grade_id == grade_id)
        .options(
            selectinload(Section.students),
            selectinload(Section.teachers),
            selectinload(Section.grade),
            selectinload(Section.student_term_records),
            selectinload(Section.teacher_term_records),
        )
    ).all()

    return sections


@router.get(
    "/{section_id}",
    response_model=SectionWithRelatedSchema,
)
def get_section_by_id(
    session: SessionDep,
    grade_id: uuid.UUID,
    section_id: uuid.UUID,
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
