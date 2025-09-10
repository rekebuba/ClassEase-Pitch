from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict

from utils.utils import to_camel

if TYPE_CHECKING:
    from .student_schema import StudentSchema
    from .student_year_record_schema import StudentYearRecordSchema
    from .yearly_subject_schema import YearlySubjectSchema


class SubjectYearlyAverageSchema(BaseModel):
    """
    This model represents the yearly average of a subject for a student.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID | None = None
    student_id: uuid.UUID
    yearly_subject_id: uuid.UUID
    student_year_record_id: Optional[uuid.UUID] = None
    average: Optional[float] = None
    rank: Optional[int] = None


class SubjectYearlyAverageRelatedSchema(BaseModel):
    """This model represents the relationships of a SubjectYearlyAverageSchema."""

    student: Optional[StudentSchema] = None
    yearly_subject: Optional[YearlySubjectSchema] = None
    student_year_record: Optional[StudentYearRecordSchema] = None
