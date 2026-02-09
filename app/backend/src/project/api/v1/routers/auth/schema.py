from pydantic import BaseModel, ConfigDict

from project.utils.utils import to_camel


class Token(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    """Schema for validating user authentication data."""

    username: str
    password: str


class LogOutResponse(BaseModel):
    message: str


class VerifyEmailResponse(BaseModel):
    message: str


class ProviderTokenResponse(BaseModel):
    token: str
