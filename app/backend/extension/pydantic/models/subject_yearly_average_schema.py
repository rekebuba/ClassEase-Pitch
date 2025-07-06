from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, ConfigDict

from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .student_schema import StudentSchema
    from .yearly_subject_schema import YearlySubjectSchema
    from .student_year_record_schema import StudentYearRecordSchema


class SubjectYearlyAverageSchema(BaseModel):
    """
    This model represents the yearly average of a subject for a student.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    student_id: str
    yearly_subject_id: str
    student_year_record_id: Optional[str] = None
    average: Optional[float] = None
    rank: Optional[int] = None


class SubjectYearlyAverageRelationshipSchema(BaseModel):
    """This model represents the relationships of a SubjectYearlyAverageSchema."""

    student: Optional[StudentSchema] = None
    yearly_subject: Optional[YearlySubjectSchema] = None
    student_year_record: Optional[StudentYearRecordSchema] = None
