import uuid
from typing import List, Optional

from pydantic import (
    EmailStr,
    PastDate,
    SecretStr,
    ValidationInfo,
    field_validator,
)
from pydantic_extra_types.phone_numbers import PhoneNumber

from project.schema.schema import BaseSchema
from project.utils.enum import (
    GenderEnum,
    PermissionEnum,
    RoleEnum,
    SchoolMembershipStatusEnum,
    SchoolStatusEnum,
    SessionScope,
)


class EmailSchema(BaseSchema):
    email: List[EmailStr]


class SchoolSummary(BaseSchema):
    id: uuid.UUID
    name: str
    slug: str
    status: SchoolStatusEnum


class MembershipSummary(BaseSchema):
    id: uuid.UUID
    school_id: uuid.UUID
    school_slug: str
    school_name: str
    status: SchoolMembershipStatusEnum
    login_identifier: Optional[str] = None
    is_primary: bool
    role_names: List[RoleEnum] = []
    shell_role: RoleEnum | None
    permissions: List[PermissionEnum] = []


class LoginTokenResponse(BaseSchema):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str
    active_school: Optional[SchoolSummary] = None
    active_membership: Optional[MembershipSummary] = None
    available_memberships: List[MembershipSummary] = []
    session_scope: SessionScope


class LoginRequest(BaseSchema):
    """Schema for validating user authentication data."""

    username: str
    password: str


class MessageResponse(BaseSchema):
    message: str


class VerifyOTPResponse(BaseSchema):
    message: str
    token: str


class ProviderResponse(BaseSchema):
    credential: Optional[str]
    school_slug: Optional[str] = None


class PasswordRecovery(BaseSchema):
    email: EmailStr


class OTPRequest(BaseSchema):
    email: EmailStr
    otp: str


class RefreshTokenRequest(BaseSchema):
    refresh_token: str
    membership_id: Optional[uuid.UUID] = None


class MembershipSelectionRequest(BaseSchema):
    membership_id: uuid.UUID


class PasswordResetRequest(BaseSchema):
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


class SignUpRequest(BaseSchema):
    first_name: str
    father_name: str
    grand_father_name: Optional[str] = None
    email: EmailStr
    phone: Optional[PhoneNumber] = None
    date_of_birth: PastDate
    gender: GenderEnum
    username: str
    password: str
