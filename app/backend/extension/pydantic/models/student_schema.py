from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, ConfigDict

from extension.enums.enum import GenderEnum
from extension.functions.helper import to_camel


if TYPE_CHECKING:
    from .user_schema import UserSchema


class StudentSchema(BaseModel):
    """
    This model represents a student in the system. It inherits from BaseModel.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    first_name: str
    father_name: str
    grand_father_name: str
    date_of_birth: str
    gender: GenderEnum

    father_phone: str
    mother_phone: str
    guardian_name: str
    guardian_phone: str

    start_year_id: str
    current_year_id: str
    current_grade_id: str
    next_grade_id: str | None = None
    semester_id: str | None = None
    has_passed: bool = False


class StudentRelationshipSchema(BaseModel):
    """This model represents the relationships of a StudentSchema."""

    user: Optional[UserSchema] = None
