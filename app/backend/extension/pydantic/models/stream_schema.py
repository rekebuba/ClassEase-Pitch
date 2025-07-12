from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List
from pydantic import BaseModel, ConfigDict

from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .grade_schema import GradeSchema
    from .yearly_subject_schema import YearlySubjectSchema
    from .student_year_record_schema import StudentYearRecordSchema


class StreamSchema(BaseModel):
    """
    This model represents a stream in the system.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: str | None = None
    year_id: str
    name: str


class StreamRelationshipSchema(BaseModel):
    """This model represents the relationships of a StreamSchema."""

    year: Optional[str] = None
    grades: Optional[List[GradeSchema]] = None
    yearly_subjects: Optional[List[YearlySubjectSchema]] = None
    students: Optional[List[StudentYearRecordSchema]] = None
