from typing import Any, Dict, Set, Tuple
import uuid
from flask import Response, jsonify
from sqlalchemy import select
from api.v1.utils.parameter import validate_expand, validate_fields
from api.v1.utils.test_parameter import query_parameters
from api.v1.utils.typing import IncEx, UserT
from api.v1.views import errors
from api.v1.views.shared import auths as auth
from api.v1.views.utils import student_teacher_or_admin_required
from extension.pydantic.models.stream_schema import (
    StreamNestedSchema,
    StreamRelatedSchema,
    StreamSchema,
    StreamWithRelatedSchema,
)
from extension.pydantic.response.schema import error_response, success_response
from models import storage
from models.grade import Grade
from models.stream import Stream


@auth.route("/grades/<uuid:grade_id>/streams", methods=["GET"])
@student_teacher_or_admin_required
@query_parameters(StreamNestedSchema)
def get_streams(
    user: UserT,
    include_params: Dict[str, Any],
    grade_id: uuid.UUID,
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

    streams_schema = [
        StreamNestedSchema.model_validate(stream).model_dump(
            by_alias=True,
            exclude_none=True,
            include=include_params,
            mode="json",
        )
        for stream in streams
    ]

    return success_response(data=streams_schema)


@auth.route("/streams/<uuid:stream_id>", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(StreamSchema, StreamSchema.default_fields())
@validate_expand(StreamRelatedSchema)
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

    stream_schema = StreamWithRelatedSchema.model_validate(stream)
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
