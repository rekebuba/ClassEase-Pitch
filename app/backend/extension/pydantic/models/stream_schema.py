from __future__ import annotations
import uuid
from typing import TYPE_CHECKING, Optional, List
from pydantic import BaseModel, ConfigDict, Field

from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .grade_schema import GradeSchema
    from .yearly_subject_schema import YearlySubjectSchema
    from .student_year_record_schema import StudentYearRecordSchema
    from .subject_schema import SubjectSchema


class StreamSchema(BaseModel):
    """
    This model represents a stream in the system.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID | None = None
    year_id: uuid.UUID
    name: str

    @classmethod
    def default_fields(cls) -> set[str]:
        """
        Returns a list of default fields to be used when no specific fields are requested.
        This can be overridden in subclasses if needed.
        """
        return {"id", "name"}


class StreamRelationshipSchema(BaseModel):
    """This model represents the relationships of a StreamSchema."""

    grade: Optional[GradeSchema] = None
    yearly_subjects: Optional[List[YearlySubjectSchema]] = None
    students: Optional[List[StudentYearRecordSchema]] = None
    subjects: List[SubjectSchema] = Field(alias="subjects")
