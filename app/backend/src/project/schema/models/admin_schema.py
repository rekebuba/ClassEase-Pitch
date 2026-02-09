from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, PastDate
from pydantic_extra_types.phone_numbers import PhoneNumber

from project.utils.enum import GenderEnum
from project.utils.utils import to_camel

if TYPE_CHECKING:
    from project.schema.models.user_schema import UserSchema


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
    date_of_birth: PastDate
    gender: GenderEnum
    phone: PhoneNumber
    email: EmailStr


class AdminRelatedSchema(BaseModel):
    """This model represents the relationships of an AdminSchema."""

    user: Optional[UserSchema] = None


class AdminWithRelatedSchema(AdminSchema, AdminRelatedSchema):
    pass
