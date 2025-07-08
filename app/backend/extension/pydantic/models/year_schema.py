from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List
from pydantic import BaseModel, ConfigDict

from extension.enums.enum import AcademicTermTypeEnum
from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .student_year_record_schema import StudentYearRecordSchema
    from .event_schema import EventSchema
    from .academic_term_schema import AcademicTermSchema
    from .yearly_subject_schema import YearlySubjectSchema


class YearSchema(BaseModel):
    """
    This model represents a year in the system.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: str | None = None
    calendar_type: AcademicTermTypeEnum
    academic_year: str
    ethiopian_year: int
    gregorian_year: Optional[str] = None


class YearRelationshipSchema(BaseModel):
    """This model represents the relationships of a YearSchema."""

    student_year_records: Optional[List[StudentYearRecordSchema]] = None
    events: Optional[List[EventSchema]] = None
    academic_terms: Optional[List[AcademicTermSchema]] = None
    yearly_subjects: Optional[List[YearlySubjectSchema]] = None
