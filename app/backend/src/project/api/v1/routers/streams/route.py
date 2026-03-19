import uuid
from typing import Annotated, List, Sequence

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from project.api.v1.routers.dependencies import SessionDep, shared_route
from project.api.v1.routers.schema import FilterParams
from project.models import GradeStreamSubject
from project.models.grade import Grade
from project.models.stream import Stream
from project.models.year import Year
from project.schema.models.stream_schema import (
    StreamSchema,
    StreamWithRelatedSchema,
)

router = APIRouter(prefix="/streams", tags=["Streams"])


@router.get(
    "",
    response_model=List[StreamSchema],
)
async def get_streams(
    session: SessionDep,
    query: Annotated[FilterParams, Query()],
    user_in: shared_route,
) -> Sequence[Stream]:
    """
    Returns specific academic grade
    """
    year = await session.get(Year, query.year_id)
    if not year:
        raise HTTPException(
            status_code=404,
            detail=f"Year with ID {query.year_id} not found.",
        )

    streams = (
        (
            await session.execute(
                select(Stream).join(Grade).where(Grade.year_id == query.year_id)
            )
        )
        .scalars()
        .all()
    )

    return streams


@router.get(
    "/{stream_id}",
    response_model=StreamSchema,
)
async def get_stream_by_id(
    session: SessionDep,
    stream_id: uuid.UUID,
    user_in: shared_route,
) -> Stream:
    """
    Returns specific academic stream
    """
    stream = await session.get(Stream, stream_id)
    if not stream:
        raise HTTPException(
            status_code=404,
            detail=f"Stream with ID {stream_id} not found.",
        )

    return stream


@router.get(
    "/{stream_id}/relation",
    response_model=StreamWithRelatedSchema,
)
async def get_stream_relation(
    session: SessionDep,
    stream_id: uuid.UUID,
    user_in: shared_route,
) -> Stream:
    """
    Returns specific academic stream with all its relationships
    """
    stream = (
        await session.execute(
            select(Stream)
            .where(Stream.id == stream_id)
            .options(
                selectinload(Stream.grade),
                selectinload(Stream.student_term_records),
                selectinload(Stream.students),
                selectinload(Stream.grade_stream_subjects).selectinload(
                    GradeStreamSubject.subject
                ),
            )
        )
    ).scalar_one_or_none()

    if not stream:
        raise HTTPException(
            status_code=404,
            detail=f"Stream with ID {stream_id} not found.",
        )

    return stream
