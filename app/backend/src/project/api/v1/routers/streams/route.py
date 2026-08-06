import uuid
from typing import Annotated, List, Sequence

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from project.api.v1.routers.dependencies import AuthenticatedRoute, SessionDep
from project.api.v1.routers.schema import FilterParams
from project.models import SubjectOffering
from project.models.grade import Grade
from project.models.stream import Stream
from project.models.year import Year
from project.schema.models.stream_schema import (
    StreamSchema,
    StreamWithRelatedSchema,
)

router = APIRouter(tags=["Streams"])


@router.get(
    "/streams",
    response_model=List[StreamSchema],
)
async def get_streams(
    session: SessionDep,
    query: Annotated[FilterParams, Query()],
    user_in: AuthenticatedRoute,
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

    streams = (await session.execute(select(Stream).join(Grade))).scalars().all()

    return streams


@router.get(
    "/streams/{stream_id}",
    response_model=StreamSchema,
)
async def get_stream_by_id(
    session: SessionDep,
    stream_id: uuid.UUID,
    user_in: AuthenticatedRoute,
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
    "/streams/{stream_id}/relation",
    response_model=StreamWithRelatedSchema,
)
async def get_stream_relation(
    session: SessionDep,
    stream_id: uuid.UUID,
    user_in: AuthenticatedRoute,
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
                selectinload(Stream.subject_offerings).selectinload(SubjectOffering.subject),
            )
        )
    ).scalar_one_or_none()

    if not stream:
        raise HTTPException(
            status_code=404,
            detail=f"Stream with ID {stream_id} not found.",
        )

    return stream
