#!/usr/bin/python3
"""Utility functions for handling API Query parameters"""

from functools import wraps
from typing import Any, Tuple, TypeVar, Callable, Type, Set
from flask import request, jsonify, Response
from pydantic import BaseModel, ConfigDict

from extension.functions.helper import to_camel, to_snake
from extension.pydantic.response.schema import ErrorResponseSchema, error_response

M = TypeVar("M", bound=BaseModel)


class InvalidFieldsResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    invalid_fields: Set[str]
    allowed_fields: Set[str]


def validate_fields(
    allowed_model: Type[M],
    default_fields: Set[str],
    field_name: str = "fields",
) -> Callable[
    [Callable[..., Tuple[Response, int]]], Callable[..., Tuple[Response, int]]
]:
    """
    Decorator to validate requested fields against a Pydantic model.

    This decorator checks if the fields requested in the 'fields' query
    parameter are valid fields defined in the `allowed_model`.

    Args:
        allowed_model: Pydantic model defining allowed fields.

    Returns:
        A decorated route function that receives a set of validated
        fields in kwargs['fields'].
    """

    def decorator(
        f: Callable[..., Tuple[Response, int]],
    ) -> Callable[..., Tuple[Response, int]]:
        @wraps(f)
        def wrapped(*args: Any, **kwargs: Any) -> Tuple[Response, int]:
            # Extract fields from query params
            requested_fields_str: str = request.args.get(field_name, "")

            requested_fields: Set[str] = {
                to_snake(field.strip())
                for field in requested_fields_str.split(",")
                if field.strip()
            }

            # Get allowed fields from the Pydantic model
            allowed_fields: Set[str] = set(allowed_model.model_fields.keys())

            # Check for any invalid fields
            invalid_fields: Set[str] = requested_fields - allowed_fields
            if invalid_fields:
                meta = InvalidFieldsResponse(
                    invalid_fields=invalid_fields,
                    allowed_fields=allowed_fields,
                )
                return error_response(
                    message="Invalid fields requested",
                    meta=meta,
                    links=None,
                    status=400,
                )

            if not requested_fields:
                # If no fields are requested, use default fields
                requested_fields = default_fields

            requested_fields.add("id")  # Ensure 'id' is always included

            dict_form = {field: ... for field in requested_fields}

            return f(*args, dict_form, **kwargs)

        return wrapped

    return decorator
