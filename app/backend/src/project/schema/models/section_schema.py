from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, ConfigDict

from project.utils.utils import to_camel

if TYPE_CHECKING:
    from project.schema.models.grade_schema import GradeSchema
    from project.schema.models.student_schema import StudentSchema
    from project.schema.models.teacher_schema import TeacherSchema


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

    @classmethod
    def default_fields(cls) -> set[str]:
        """
        Returns a list of default fields to be used when no specific fields are requested.
        This can be overridden in subclasses if needed.
        """
        return {"id", "section"}


class SectionRelatedSchema(BaseModel):
    """This model represents the relationships of a SectionSchema."""

    grade: Optional[GradeSchema] = None
    students: Optional[List[StudentSchema]] = []
    teachers: Optional[List[TeacherSchema]] = []


class SectionWithRelatedSchema(SectionSchema, SectionRelatedSchema):
    """This model represents a SectionSchema with its relationships."""

    pass
