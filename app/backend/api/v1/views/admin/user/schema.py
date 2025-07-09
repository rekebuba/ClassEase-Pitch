from typing import Optional
import bcrypt
from pydantic import BaseModel, ConfigDict, field_validator

from extension.enums.enum import RoleEnum
from extension.functions.helper import to_camel


class NewUserSchema(BaseModel):
    """
    Schema for creating a new user.
    This schema is used for both student, teacher and admin.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    academic_id: str
    identification: Optional[str] = None
    password: Optional[str] = None
    role: RoleEnum

    @field_validator("password")
    @classmethod
    def hash_password(cls, raw_password: Optional[str]) -> str | None:
        """Hashes the password using bcrypt."""
        if not raw_password:
            return None

        return bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )


class SucssussfulLinkResponse(BaseModel):
    """
    Schema for successful user role link response.
    """

    message: str
    id: str
