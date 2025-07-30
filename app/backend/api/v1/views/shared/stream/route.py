from typing import Set, Tuple
import uuid
from flask import Response, jsonify
from sqlalchemy import select
from api.v1.utils.parameter import validate_expand, validate_fields
from api.v1.utils.typing import IncEx, UserT
from api.v1.views import errors
from api.v1.views.shared import auths as auth
from api.v1.views.utils import student_teacher_or_admin_required
from extension.pydantic.models.stream_schema import (
    StreamRelationshipSchema,
    StreamSchema,
    StreamWithRelationshipSchema,
)
from extension.pydantic.response.schema import error_response, success_response
from models import storage
from models.grade import Grade
from models.stream import Stream


@auth.route("/grades/<uuid:grade_id>/streams", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(StreamSchema, StreamSchema.default_fields())
def get_streams(
    user: UserT, fields: Set[str], grade_id: uuid.UUID
) -> Tuple[Response, int]:
    """
    Get all streams.

    Returns:
        Tuple[Response, int]: JSON response with streams and status code.
    """
    if not storage.session.get(Grade, grade_id):
        return error_response(
            message=f"Grade with ID {grade_id} not found.", status=404
        )

    streams = storage.session.scalars(
        select(Stream).where(Stream.grade_id == grade_id)
    ).all()

    streams_schema = [StreamSchema.model_validate(stream) for stream in streams]
    stream_response = [
        stream_schema.model_dump(
            by_alias=True,
            exclude_none=True,
            include=fields,
            mode="json",
        )
        for stream_schema in streams_schema
    ]

    return success_response(data=stream_response)


@auth.route("/streams/<uuid:stream_id>", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(StreamSchema, StreamSchema.default_fields())
@validate_expand(StreamRelationshipSchema)
def get_stream_by_id(
    user: UserT,
    fields: dict[str, IncEx],
    related_fields: dict[str, IncEx],
    stream_id: uuid.UUID,
) -> Tuple[Response, int]:
    """
    Get a stream by its ID.

    Args:
        stream_id (str): The ID of the stream.
    """
    stream = storage.session.scalar(select(Stream).where(Stream.id == stream_id))
    if not stream:
        return errors.handle_not_found_error(message="Stream not found")

    stream_schema = StreamWithRelationshipSchema.model_validate(stream)
    stream_response = stream_schema.model_dump(
        by_alias=True,
        exclude_none=True,
        include={
            **fields,
            **related_fields,
        },
        mode="json",
    )

    return success_response(data=stream_response)
