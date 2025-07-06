from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List
from pydantic import BaseModel, ConfigDict

from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .student_schema import StudentSchema
    from .grade_schema import GradeSchema
    from .year_schema import YearSchema
    from .stream_schema import StreamSchema
    from .student_term_record_schema import StudentTermRecordSchema
    from .subject_yearly_average_schema import SubjectYearlyAverageSchema


class StudentYearRecordSchema(BaseModel):
    """
    This model represents a student's yearly academic record.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    student_id: str
    grade_id: str
    year_id: str
    stream_id: Optional[str] = None
    final_score: Optional[float] = None
    rank: Optional[int] = None


class StudentYearRecordRelationshipSchema(BaseModel):
    """This model represents the relationships of a StudentYearRecordSchema."""

    student: Optional[StudentSchema] = None
    grade: Optional[GradeSchema] = None
    year: Optional[YearSchema] = None
    stream: Optional[StreamSchema] = None
    student_term_records: Optional[List[StudentTermRecordSchema]] = None
    subject_yearly_averages: Optional[List[SubjectYearlyAverageSchema]] = None
