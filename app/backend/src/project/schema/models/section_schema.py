from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List

from pydantic import BaseModel, ConfigDict

from project.utils.utils import to_camel

if TYPE_CHECKING:
    from project.schema.models.grade_schema import GradeSchema
    from project.schema.models.student_schema import StudentSchema


class SectionSchema(BaseModel):
    """
    This model represents a section in the system.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    grade_id: uuid.UUID
    section: str


class SectionRelatedSchema(BaseModel):
    """This model represents the relationships of a SectionSchema."""

    grade: GradeSchema
    students: List[StudentSchema]
    # teachers: List[TeacherSchema]


class SectionWithRelatedSchema(SectionSchema, SectionRelatedSchema):
    """This model represents a SectionSchema with its relationships."""

    pass
