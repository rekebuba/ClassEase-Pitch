from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from .user_schema import UserSchema


class AdminSchema(BaseModel):
    """
    This model represents an admin in the system. It inherits from BaseModel.
    """

    model_config = ConfigDict(from_attributes=True)

    user_id: str
    first_name: str
    father_name: str
    grand_father_name: str
    date_of_birth: str
    gender: str
    email: str
    phone: str
    address: str


class AdminRelationshipSchema(BaseModel):
    """This model represents the relationships of an AdminSchema."""

    user: Optional[UserSchema] = None
