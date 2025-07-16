from __future__ import annotations
import uuid
from typing import TYPE_CHECKING, Optional, List
from pydantic import BaseModel, ConfigDict

from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .student_term_record_schema import StudentTermRecordSchema
    from .teacher_record_schema import TeacherRecordSchema
    from .grade_schema import GradeSchema


class SectionSchema(BaseModel):
    """
    This model represents a section in the system.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID | None = None
    year_id: uuid.UUID
    section: Optional[str] = None

    @classmethod
    def default_fields(cls) -> set[str]:
        """
        Returns a list of default fields to be used when no specific fields are requested.
        This can be overridden in subclasses if needed.
        """
        return {"id", "section"}


class SectionRelationshipSchema(BaseModel):
    """This model represents the relationships of a SectionSchema."""

    year: Optional[str] = None
    student_term_records: List[StudentTermRecordSchema] = []
    teacher_records_link: List[TeacherRecordSchema] = []
    grades_link: List[GradeSchema] = []


class SectionSchemaWithRelationships(SectionSchema):
    """This model represents a SectionSchema with its relationships."""

    pass
