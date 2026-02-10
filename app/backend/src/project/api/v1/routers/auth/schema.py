from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr

from project.utils.utils import to_camel


class LoginTokenResponse(BaseModel):
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


class MessageResponse(BaseModel):
    message: str


class VerifyOTPResponse(BaseModel):
    message: str
    token: str


class ProviderTokenResponse(BaseModel):
    token: str


class OTPRequest(BaseModel):
    email: EmailStr
    otp: str


class PasswordResetRequest(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    email: EmailStr
    token: str
    new_password: SecretStr
