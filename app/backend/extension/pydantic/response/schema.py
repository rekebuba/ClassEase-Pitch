from typing import Any, Dict, Generic, List, Optional, Tuple, TypeVar, Union
from flask import Response, jsonify
from pydantic import BaseModel, ConfigDict, Field

from extension.functions.helper import to_camel

T = TypeVar("T")  # For the data payload
M = TypeVar("M")  # For meta
L = TypeVar("L")  # For links


class SuccessResponseSchema(BaseModel, Generic[T, M, L]):
    """
    This model represents a generic response schema.
    It can be used to standardize the structure of API responses.
    """

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    data: T
    message: str = "Success"
    meta: Optional[M] = None
    links: Optional[L] = None


class ErrorResponseSchema(BaseModel, Generic[M, L]):
    """
    This model represents an error response schema.
    It can be used to standardize the structure of API error responses.
    """

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    message: str
    meta: Optional[M] = None
    links: Optional[L] = None


class ValidationErrorSchema(BaseModel):
    """
    To transform and sanitize raw Pydantic error entries to a more user-friendly format.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )
    location: str
    message: str
    input: Any
    expected_type: str
    expected: Optional[Any] = None  # will be populated manually from ctx


def success_response(
    data: Union[BaseModel, List[BaseModel], Dict[str, Any], List[Dict[str, Any]]],
    message: str = "Success",
    meta: Optional[BaseModel] = None,
    links: Optional[BaseModel] = None,
    status: int = 200,
) -> Tuple[Response, int]:
    return (
        jsonify(
            SuccessResponseSchema(
                data=data, message=message, meta=meta, links=links
            ).model_dump(exclude_none=True, by_alias=True, mode="json"),
        ),
        status,
    )


def error_response(
    message: str,
    meta: Optional[
        Union[BaseModel, List[BaseModel], Dict[str, Any], List[Dict[str, Any]]]
    ] = None,
    links: Optional[BaseModel] = None,
    status: int = 400,
) -> Tuple[Response, int]:
    return (
        jsonify(
            ErrorResponseSchema(message=message, meta=meta, links=links).model_dump(
                exclude_none=True, by_alias=True, mode="json"
            ),
        ),
        status,
    )
