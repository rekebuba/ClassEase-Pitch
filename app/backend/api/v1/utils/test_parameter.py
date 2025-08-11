#!/usr/bin/python3
"""
Utility functions for handling and validating API query parameters,
specifically for parsing 'expand' and 'fields' into a structure
suitable for Pydantic model dumping.
"""

from functools import wraps
from typing import Any, Dict, List, Set, Tuple, TypeVar, Callable, Type
from flask import request, Response
from pydantic import BaseModel, ConfigDict

from extension.functions.helper import (
    classify_model_fields,
    extract_inner_model,
    to_camel,
)
from extension.pydantic.response.schema import error_response

M = TypeVar("M", bound=BaseModel)


class InvalidFieldsResponse(BaseModel):
    """Response model for reporting invalid expand requests."""

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    invalid_fields: Set[str]
    allowed_fields: Set[str]


def _parse_nested_params(
    base_model: Type[BaseModel], prefix: str = ""
) -> Tuple[Response, int] | Dict[str, Any]:
    """
    Recursively parses 'expand' and 'fields' query parameters into a
    nested dictionary that Pydantic's `model_dump(include=...)` can consume.

    This function validates expansion fields and ensures that error
    responses are propagated correctly.
    """
    expand_value = request.args.get("expand", "")
    fields_value = request.args.get("fields", "")

    # Filter only relevant expansions for this prefix
    expansions = {
        e[len(prefix) + 1 :] if prefix else e
        for e in expand_value.split(",")
        if e.strip() and (not prefix or e.startswith(prefix + ".") or e == prefix)
    }
    if expansions == {""}:
        expansions = set()

    # Filter only relevant fields for this prefix
    field_names = {
        f[len(prefix) + 1 :] if prefix else f
        for f in fields_value.split(",")
        if f.strip() and (not prefix or f.startswith(prefix + ".") or f == prefix)
    }
    if field_names == {""}:
        field_names = set()

    classified = classify_model_fields(base_model)
    allowed_fields = set(classified.get("model_class", []))

    valid_fields: List[str] = []
    for field in field_names:
        # Validate that the field is a model class
        if field == "all":
            valid_fields.extend(allowed_fields)
            break

        if field not in allowed_fields and "." in field and not expansions:
            # Nested field without expansion -> invalid
            allowed_fields.add("all")
            meta = InvalidFieldsResponse(
                invalid_fields={field}, allowed_fields=allowed_fields
            )
            return error_response(
                message="Invalid field requested", status=400, meta=meta
            )
        elif "." not in field:
            valid_fields.append(field)

    # If no fields explicitly given for this model, use defaults
    if not valid_fields:
        if hasattr(base_model, "default_fields"):
            valid_fields = list(base_model.default_fields())
        else:
            valid_fields = list(base_model.model_fields.keys())

    if "id" in base_model.model_fields:
        valid_fields.append("id")  # insure id is always included

    include_dict: Dict[str, Any] = {f: ... for f in valid_fields}

    # Process expansions
    allowed_expansions = set(classified.get("model_sub_class", []))
    for exp in expansions:
        if exp == "":
            continue

        expand, rest = exp.split(".", 1) if "." in exp else (exp, None)

        # Validate that the expansion expand is a model subclass
        if expand not in allowed_expansions:
            meta = InvalidFieldsResponse(
                invalid_fields={expand}, allowed_fields=allowed_expansions
            )
            return error_response(
                message="Invalid expand requested", status=400, meta=meta
            )

        is_list, related_model = extract_inner_model(
            base_model.model_fields[expand].annotation
        )
        # Build nested prefix for child expansion
        child_prefix = f"{prefix}.{expand}" if prefix else expand

        nested_params = _parse_nested_params(related_model, prefix=child_prefix)

        if isinstance(nested_params, tuple):
            return nested_params

        include_dict[expand] = {"__all__": nested_params} if is_list else nested_params

    return include_dict


def query_parameters(
    model: Type[M],
) -> Callable[
    [Callable[..., Tuple[Response, int]]], Callable[..., Tuple[Response, int]]
]:
    """
    Decorator to parse 'expand' and 'fields' query params, injecting an
    'include_params' dictionary into the decorated function.
    """

    def decorator(
        f: Callable[..., Tuple[Response, int]],
    ) -> Callable[..., Tuple[Response, int]]:
        @wraps(f)
        def wrapped(*args: Any, **kwargs: Any) -> Tuple[Response, int]:
            include_params = _parse_nested_params(model)
            if isinstance(include_params, tuple):  # Error response
                return include_params
            return f(*args, **kwargs, include_params=include_params)

        return wrapped

    return decorator
