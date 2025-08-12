from __future__ import annotations
import uuid
from typing import TYPE_CHECKING, Optional, List
from pydantic import BaseModel, ConfigDict

from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .year_schema import YearSchema
    from .subject_schema import SubjectSchema
    from .grade_schema import GradeSchema
    from .stream_schema import StreamSchema
    from .assessment_schema import AssessmentSchema
    from .subject_yearly_average_schema import SubjectYearlyAverageSchema
    from .teacher_record_schema import TeacherRecordSchema


class YearlySubjectSchema(BaseModel):
    """
    This model represents a yearly subject in the system.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID | None = None
    year_id: Optional[uuid.UUID] = None
    subject_id: uuid.UUID
    grade_id: uuid.UUID
    stream_id: Optional[uuid.UUID] = None
    subject_code: str


class YearlySubjectRelatedSchema(BaseModel):
    """This model represents the relationships of a YearlySubjectSchema."""

    year: Optional[YearSchema] = None
    subject: Optional[SubjectSchema] = None
    grade: Optional[GradeSchema] = None
    stream: Optional[StreamSchema] = None
    assessments: Optional[List[AssessmentSchema]] = None
    subject_yearly_averages: Optional[List[SubjectYearlyAverageSchema]] = None
    teacher_records_link: Optional[List[TeacherRecordSchema]] = None
