#!/usr/bin/python3
"""Utility functions for handling API Query parameters"""

from functools import wraps
from types import EllipsisType
from typing import Any, Dict, Tuple, TypeVar, Callable, Type, Set
from flask import request, Response
from pydantic import BaseModel, ConfigDict
from extension.functions.helper import extract_inner_model, to_camel, to_snake
from extension.pydantic.response.schema import error_response

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


def _extract_and_validate_fields(
    allowed_model: Type[M],
    field_name: str,
    error_message: str,
) -> Tuple[Response, int] | Set[str]:
    """Helper function to extract and validate fields from query parameters."""
    requested_fields_str: str = request.args.get(field_name, "")
    requested_fields: Set[str] = {
        to_snake(field.strip())
        for field in requested_fields_str.split(",")
        if field.strip()
    }

    allowed_fields: Set[str] = set(allowed_model.model_fields.keys())

    invalid_fields: Set[str] = requested_fields - allowed_fields
    if invalid_fields:
        meta = InvalidFieldsResponse(
            invalid_fields=invalid_fields,
            allowed_fields=allowed_fields,
        )
        return error_response(
            message=error_message,
            meta=meta,
            links=None,
            status=400,
        )

    return requested_fields


def create_query_param_validator(
    allowed_model: Type[M],
    default_fields: Set[str],
    field_name: str,
    error_message: str,
    process_func: Callable[[Set[str], Type[M], Set[str]], Any],
) -> Callable[
    [Callable[..., Tuple[Response, int]]], Callable[..., Tuple[Response, int]]
]:
    """
    Factory for creating decorators that validate and process query parameters.
    """

    def decorator(
        f: Callable[..., Tuple[Response, int]],
    ) -> Callable[..., Tuple[Response, int]]:
        @wraps(f)
        def wrapped(*args: Any, **kwargs: Any) -> Tuple[Response, int]:
            validated_fields = _extract_and_validate_fields(
                allowed_model, field_name, error_message
            )
            if isinstance(validated_fields, tuple):  # Error response
                return validated_fields

            processed_data = process_func(
                validated_fields, allowed_model, default_fields
            )
            return f(*args, processed_data, **kwargs)

        return wrapped

    return decorator


def _process_fields(
    requested_fields: Set[str], _: Type[M], default_fields: Set[str]
) -> Dict[str, EllipsisType]:
    """Processing function for `validate_fields`."""
    if not requested_fields:
        requested_fields = default_fields
    requested_fields.add("id")  # Ensure 'id' is always included
    return {field: ... for field in requested_fields}


def _process_expand(
    requested_expand: Set[str],
    allowed_model: Type[M],
    default_fields: Set[str],
) -> Dict[str, Any]:
    """Processing function for `validate_expand`."""
    nested_fields: Dict[str, Any] = {}
    for field in requested_expand:
        is_list, model = extract_inner_model(
            allowed_model.model_fields[field].annotation
        )
        valid_fields = _extract_and_validate_fields(
            model, f"{field}_fields", "Invalid fields requested"
        )
        processed = _process_fields(
            valid_fields if isinstance(valid_fields, set) else set(),
            model,
            model.default_fields()
            if hasattr(model, "default_fields")
            else default_fields,
        )

        nested_fields[field] = {"__all__": processed} if is_list else processed

    return nested_fields


def validate_fields(
    allowed_model: Type[M],
    default_fields: Set[str],
    field_name: str = "fields",
) -> Callable[
    [Callable[..., Tuple[Response, int]]], Callable[..., Tuple[Response, int]]
]:
    """
    Decorator to validate requested fields against a Pydantic model.
    """
    return create_query_param_validator(
        allowed_model=allowed_model,
        default_fields=default_fields,
        field_name=field_name,
        error_message="Invalid fields requested",
        process_func=_process_fields,
    )


def validate_expand(
    allowed_model: Type[M],
    default_fields: Set[str] = set(),
    field_name: str = "expand",
) -> Callable[
    [Callable[..., Tuple[Response, int]]], Callable[..., Tuple[Response, int]]
]:
    """
    Decorator to validate requested expand against a Pydantic model.
    """
    return create_query_param_validator(
        allowed_model=allowed_model,
        default_fields=default_fields,
        field_name=field_name,
        error_message="Invalid expand requested",
        process_func=_process_expand,
    )
