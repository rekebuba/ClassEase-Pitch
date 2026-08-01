import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from project.utils.enum import RoleEnum, SessionScope


class BaseSchema(BaseModel):
    """
    This model serves as a base schema for other Pydantic models.
    It provides common configuration settings that can be inherited by other models.
    """

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )


class SuccessResponseSchema(BaseSchema):
    """
    This model represents a generic response schema.
    It can be used to standardize the structure of API responses.
    """

    id: uuid.UUID | None = None
    message: str = "Success"


class SuccessMessage(BaseSchema):
    message: str


class SuccessResponse(BaseSchema):
    message: str
    id: uuid.UUID


class ErrorResponseSchema(BaseSchema):
    """
    This model represents an error response schema.
    It can be used to standardize the structure of API error responses.
    """

    message: str


class TokenPayload(BaseSchema):
    exp: datetime
    sub: str
    role: RoleEnum | None = None
    scope: SessionScope = SessionScope.SCHOOL
    school_id: uuid.UUID | None = None
    school_slug: str | None = None
    membership_id: uuid.UUID | None = None
    session_id: uuid.UUID | None = None
    permissions_version: int | None = None
    permissions: list[str] = Field(default_factory=list)
    mfa_state: str | None = None
    jti: uuid.UUID
    iat: datetime
