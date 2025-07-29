from __future__ import annotations
import uuid
from typing import TYPE_CHECKING, Optional, List
from pydantic import BaseModel, ConfigDict

from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .student_term_record_schema import StudentTermRecordSchema
    from .teacher_term_record_schema import TeacherTermRecordSchema
    from .grade_schema import GradeSchema
    from .student_schema import StudentSchema
    from .teacher_schema import TeacherSchema


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
    grade_id: uuid.UUID
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

    teacher_term_records: Optional[List[TeacherTermRecordSchema]] = []
    student_term_records: Optional[List[StudentTermRecordSchema]] = []
    grade: Optional[GradeSchema] = None
    students: Optional[List[StudentSchema]] = []
    teachers: Optional[List[TeacherSchema]] = []


class SectionSchemaWithRelationships(SectionSchema, SectionRelationshipSchema):
    """This model represents a SectionSchema with its relationships."""

    pass
