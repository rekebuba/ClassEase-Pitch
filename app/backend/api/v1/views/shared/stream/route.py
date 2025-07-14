from typing import Set, Tuple
from flask import Response, jsonify
from pydantic import ValidationError
from sqlalchemy import select
from api.v1.utils.parameter import validate_fields
from api.v1.utils.typing import UserT
from api.v1.views import errors
from api.v1.views.shared import auths as auth
from api.v1.views.utils import student_teacher_or_admin_required
from extension.pydantic.models.stream_schema import StreamSchema
from extension.pydantic.response.schema import success_response
from models import storage
from models.stream import Stream


@auth.route("/years/<string:year_id>/streams", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(StreamSchema, StreamSchema.default_fields())
def get_streams(user: UserT, fields: Set[str], year_id: str) -> Tuple[Response, int]:
    """
    Get all streams.

    Returns:
        Tuple[Response, int]: JSON response with streams and status code.
    """
    try:
        streams = storage.session.scalars(
            select(Stream).where(Stream.year_id == year_id)
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

    except ValidationError as e:
        return errors.handle_validation_error(error=e)
    except Exception as e:
        return errors.handle_internal_error(error=e)


@auth.route("/years/<string:year_id>/streams/<string:stream_id>", methods=["GET"])
@student_teacher_or_admin_required
@validate_fields(StreamSchema, StreamSchema.default_fields())
def get_stream_by_id(
    user: UserT,
    fields: Set[str],
    year_id: str,
    stream_id: str,
) -> Tuple[Response, int]:
    """
    Get a stream by its ID.

    Args:
        stream_id (str): The ID of the stream.
    """
    try:
        stream = storage.session.scalar(
            select(Stream).where(Stream.id == stream_id, Stream.year_id == year_id)
        )
        if not stream:
            return errors.handle_not_found_error(message="Stream not found")

        stream_schema = StreamSchema.model_validate(stream)
        stream_response = stream_schema.model_dump(
            by_alias=True,
            exclude_none=True,
            include=fields,
            mode="json",
        )

        return success_response(data=stream_response)

    except ValidationError as e:
        return errors.handle_validation_error(error=e)
    except Exception as e:
        return errors.handle_internal_error(error=e)
