from __future__ import annotations
import uuid
from datetime import date
from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, ConfigDict

from extension.enums.enum import GenderEnum
from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .user_schema import UserSchema


class AdminSchema(BaseModel):
    """
    This model represents an admin in the system. It inherits from BaseModel.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID | None = None
    user_id: Optional[uuid.UUID] = None
    first_name: str
    father_name: str
    grand_father_name: str
    date_of_birth: date
    gender: GenderEnum
    email: str
    phone: str
    address: str

    @classmethod
    def default_fields(cls) -> set[str]:
        return {
            "id",
            "first_name",
            "father_name",
            "grand_father_name",
        }


class AdminRelationshipSchema(BaseModel):
    """This model represents the relationships of an AdminSchema."""

    user: Optional[UserSchema] = None


class AdminWithRelationshipsSchema(AdminSchema, AdminRelationshipSchema):
    pass
