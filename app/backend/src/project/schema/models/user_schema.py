from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List, Optional

from pydantic import AwareDatetime, BaseModel, ConfigDict

from project.utils.enum import RoleEnum
from project.utils.utils import to_camel

if TYPE_CHECKING:
    from project.schema.models.admin_schema import AdminSchema
    from project.schema.models.saved_query_view_schema import SavedQueryViewSchema
    from project.schema.models.student_schema import StudentSchema
    from project.schema.models.teacher_schema import TeacherSchema


class UserSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    identification: str
    role: RoleEnum
    image_path: Optional[str] = None
    created_at: AwareDatetime

    @classmethod
    def default_fields(cls) -> set[str]:
        return {
            "id",
            "identification",
            "role",
            "imagePath",
        }


class UserRelatedSchema(BaseModel):
    """This model represents the relationships of a UserSchema.
    It is used to define the relationships between the UserSchema and other schemas.
    """

    admin: Optional[AdminSchema] = None
    teacher: Optional[TeacherSchema] = None
    student: Optional[StudentSchema] = None
    saved_query_views: Optional[List[SavedQueryViewSchema]] = None


class UserWithRelatedSchema(UserSchema, UserRelatedSchema):
    pass
