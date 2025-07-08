from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from extension.enums.enum import RoleEnum
from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .admin_schema import AdminSchema
    from .teacher_schema import TeacherSchema
    from .student_schema import StudentSchema
    from .saved_query_view_schema import SavedQueryViewSchema


class UserSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: str | None = None
    identification: str
    password: str
    role: RoleEnum
    national_id: str
    image_path: Optional[str] = None
    created_at: Optional[datetime] = None


class UserRelationshipSchema(BaseModel):
    """This model represents the relationships of a UserSchema.
    It is used to define the relationships between the UserSchema and other schemas.
    """

    admins: Optional[AdminSchema] = None
    teachers: Optional[TeacherSchema] = None
    students: Optional[StudentSchema] = None
    saved_query_views: Optional[List[SavedQueryViewSchema]] = None
