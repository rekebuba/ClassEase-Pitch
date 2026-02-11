from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    SecretStr,
    ValidationInfo,
    field_validator,
)

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


class ProviderResponse(BaseModel):
    credential: Optional[str]


class PasswordRecovery(BaseModel):
    email: EmailStr


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
    confirm_password: SecretStr

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v: SecretStr, info: ValidationInfo) -> SecretStr:
        # info.data contains the values of previously validated fields
        if "new_password" in info.data:
            new_pass = info.data["new_password"].get_secret_value()
            if v.get_secret_value() != new_pass:
                raise ValueError("Passwords do not match")
        return v
