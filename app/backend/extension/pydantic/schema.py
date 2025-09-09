from datetime import datetime
from typing import Generic, Optional, Set, TypeVar
import uuid
from pydantic import BaseModel, ConfigDict

from extension.enums.enum import RoleEnum
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


class TokenPayload(BaseModel):
    exp: datetime
    sub: str
    role: RoleEnum
    jti: uuid.UUID
    iat: datetime
