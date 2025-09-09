import uuid
from typing import Annotated, List, Sequence

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select

from api.v1.routers.dependencies import SessionDep
from api.v1.routers.schema import FilterParams
from extension.pydantic.models.stream_schema import (
    StreamSchema,
)
from models.grade import Grade
from models.stream import Stream
from models.year import Year

router = APIRouter(prefix="/streams", tags=["Streams"])


@router.get(
    "/",
    response_model=List[StreamSchema],
)
def get_streams(
    session: SessionDep,
    query: Annotated[FilterParams, Query()],
) -> Sequence[Stream]:
    """
    Returns specific academic grade
    """
    year = session.get(Year, query.year_id)
    if not year:
        raise HTTPException(
            status_code=404,
            detail=f"Year with ID {query.year_id} not found.",
        )

    streams = session.scalars(
        select(Stream).join(Grade).where(Grade.year_id == query.year_id)
    ).all()

    return streams


@router.get(
    "/{stream_id}",
    response_model=StreamSchema,
)
def get_stream_by_id(
    session: SessionDep,
    stream_id: uuid.UUID,
) -> Stream:
    """
    Returns specific academic stream
    """
    stream = session.get(Stream, stream_id)
    if not stream:
        raise HTTPException(
            status_code=404,
            detail=f"Stream with ID {stream_id} not found.",
        )

    return stream
