from enum import Enum
import inspect
from typing import Set, Tuple

from flask import Response, request
from api.v1.utils.typing import UserT
from api.v1.views.shared import auths as auth
from api.v1.views.utils import student_teacher_or_admin_required
from extension.functions.helper import to_camel, to_snake
from extension.pydantic.response.schema import error_response, success_response
from extension.enums import enum


@auth.route("/suggestion", methods=["GET"])
@student_teacher_or_admin_required
def get_suggested_grades(user: UserT) -> Tuple[Response, int]:
    """
    Returns a list of suggested grades based on predefined Enum values.
    """
    requested_fields_str: str = request.args.get("fields", "")
    requested_fields: Set[str] = {
        to_snake(field.strip())
        for field in requested_fields_str.split(",")
        if field.strip()
    }

    allowed_enum = {
        to_snake(name).removesuffix("_enum"): getattr(enum, name)
        for name in dir(enum)
        if inspect.isclass(getattr(enum, name))
        and issubclass(getattr(enum, name), Enum)
    }
    allowed_enum.pop("enum", None)  # Remove the base Enum class if present

    if len(requested_fields) == 1 and "all" in requested_fields:
        requested_fields = set(allowed_enum.keys())

    if not requested_fields:
        return error_response(
            message="No fields requested",
            meta={"allowedFields": list(allowed_enum.keys())},
            status=400,
        )

    if not requested_fields.issubset(allowed_enum.keys()):
        return error_response(
            message="Invalid enum fields requested",
            meta={
                "invalidFields": requested_fields - set(allowed_enum.keys()),
                "allowedFields": set(allowed_enum.keys()),
            },
            status=400,
        )

    result = {
        to_camel(field): [enum.value for enum in allowed_enum[field]]
        for field in requested_fields
    }

    return success_response(data=result)
