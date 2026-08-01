from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Optional

from pydantic import PastDate

from project.schema.schema import BaseSchema
from project.utils.enum import GenderEnum

if TYPE_CHECKING:
    from project.schema.models.user_schema import UserSchema


class AdminSchema(BaseSchema):
    """
    This model represents an admin in the system. It inherits from BaseModel.
    """

    id: uuid.UUID | None = None
    user_id: Optional[uuid.UUID] = None
    first_name: str
    father_name: str
    grand_father_name: str
    date_of_birth: PastDate
    gender: GenderEnum


class AdminRelatedSchema(BaseSchema):
    """This model represents the relationships of an AdminSchema."""

    user: Optional[UserSchema] = None


class AdminWithRelatedSchema(AdminSchema, AdminRelatedSchema):
    pass
