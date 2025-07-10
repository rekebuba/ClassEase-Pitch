from typing import Tuple
from flask import Response, jsonify
from pydantic import ValidationError
from sqlalchemy import select
from api.v1.utils.typing import UserT
from api.v1.views import errors
from api.v1.views.shared import auths as auth
from api.v1.views.utils import student_teacher_or_admin_required
from extension.pydantic.models.stream_schema import StreamSchema
from models import storage
from models.stream import Stream


@auth.route("/streams", methods=["GET"])
@student_teacher_or_admin_required
def get_streams(user: UserT) -> Tuple[Response, int]:
    """
    Get all streams.

    Returns:
        Tuple[Response, int]: JSON response with streams and status code.
    """
    try:
        streams = storage.session.scalars(select(Stream)).all()
        streams_schema = [StreamSchema.model_validate(stream) for stream in streams]
        response = [
            stream_schema.model_dump(by_alias=True, exclude_none=True)
            for stream_schema in streams_schema
        ]
        return jsonify(response), 200

    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)


@auth.route("/streams/<string:stream_id>", methods=["GET"])
@student_teacher_or_admin_required
def get_stream_by_id(user: UserT, stream_id: str) -> Tuple[Response, int]:
    """
    Get a stream by its ID.

    Args:
        stream_id (str): The ID of the stream.
    """
    try:
        stream = storage.session.get(Stream, stream_id)
        if not stream:
            return errors.handle_not_found_error("Stream not found")

        stream_schema = StreamSchema.model_validate(stream)
        return jsonify(stream_schema.model_dump(by_alias=True, exclude_none=True)), 200

    except ValidationError as e:
        return errors.handle_validation_error(e)
    except Exception as e:
        return errors.handle_internal_error(e)
