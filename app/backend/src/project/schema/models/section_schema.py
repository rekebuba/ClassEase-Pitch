from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List

from project.schema.schema import BaseSchema

if TYPE_CHECKING:
    from project.schema.models.grade_schema import GradeSchema
    from project.schema.models.student_schema import StudentSchema


class SectionSchema(BaseSchema):
    """
    This model represents a section in the system.
    """

    id: uuid.UUID
    grade_id: uuid.UUID
    section: str


class SectionRelatedSchema(BaseSchema):
    """This model represents the relationships of a SectionSchema."""

    grade: GradeSchema
    students: List[StudentSchema]
    # teachers: List[TeacherSchema]


class SectionWithRelatedSchema(SectionSchema, SectionRelatedSchema):
    """This model represents a SectionSchema with its relationships."""

    pass
