from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List, Optional

from pydantic import AwareDatetime, EmailStr, PastDate
from pydantic_extra_types.phone_numbers import PhoneNumber

from project.schema.schema import BaseSchema
from project.utils.enum import GenderEnum

if TYPE_CHECKING:
    from project.schema.models.admin_schema import AdminSchema
    from project.schema.models.saved_query_view_schema import SavedQueryViewSchema
    from project.schema.models.student_schema import StudentSchema
    from project.schema.models.teacher_schema import TeacherSchema


class UserSchema(BaseSchema):
    id: uuid.UUID
    username: str
    first_name: str
    father_name: str
    grand_father_name: str | None
    date_of_birth: PastDate
    gender: GenderEnum
    email: EmailStr | None
    phone: PhoneNumber | None
    image_path: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: AwareDatetime
    updated_at: AwareDatetime


class UserRelatedSchema(BaseSchema):
    """This model represents the relationships of a UserSchema.
    It is used to define the relationships between the UserSchema and other schemas.
    """

    admin: Optional[AdminSchema] = None
    teacher: Optional[TeacherSchema] = None
    student: Optional[StudentSchema] = None
    saved_query_views: Optional[List[SavedQueryViewSchema]] = None


class UserWithRelatedSchema(UserSchema, UserRelatedSchema):
    pass
