from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List
from pydantic import BaseModel, ConfigDict

from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .student_term_record_schema import StudentTermRecordSchema
    from .teacher_record_schema import TeacherRecordSchema


class SectionSchema(BaseModel):
    """
    This model represents a section in the system.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: str | None = None
    section: Optional[str] = None


class SectionRelationshipSchema(BaseModel):
    """This model represents the relationships of a SectionSchema."""

    student_term_records: Optional[List[StudentTermRecordSchema]] = None
    teacher_records_link: Optional[List[TeacherRecordSchema]] = None
