import uuid
from typing import List, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    SecretStr,
    ValidationInfo,
    field_validator,
)

from project.utils.enum import RoleEnum, SchoolMembershipStatusEnum, SchoolStatusEnum
from project.utils.utils import to_camel


class SchoolSummary(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    name: str
    slug: str
    status: SchoolStatusEnum


class MembershipSummary(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    school_id: uuid.UUID
    school_slug: str
    school_name: str
    status: SchoolMembershipStatusEnum
    login_identifier: Optional[str] = None
    is_primary: bool
    role_names: List[str] = []
    shell_role: RoleEnum
    permissions: List[str] = []


class LoginTokenResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    access_token: str
    refresh_token: Optional[str] = None
    token_type: str
    active_school: Optional[SchoolSummary] = None
    active_membership: Optional[MembershipSummary] = None
    available_memberships: List[MembershipSummary] = []


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
    school_slug: Optional[str] = None


class PasswordRecovery(BaseModel):
    email: EmailStr


class OTPRequest(BaseModel):
    email: EmailStr
    otp: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class MembershipSelectionRequest(BaseModel):
    membership_id: uuid.UUID


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
