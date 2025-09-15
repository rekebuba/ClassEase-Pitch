import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from utils.enum import RoleEnum
from utils.utils import to_camel


class SuccessResponseSchema(BaseModel):
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

    message: str = "Success"


class ErrorResponseSchema(BaseModel):
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


class TokenPayload(BaseModel):
    exp: datetime
    sub: str
    role: RoleEnum
    jti: uuid.UUID
    iat: datetime
