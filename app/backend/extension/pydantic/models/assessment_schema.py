from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, ConfigDict

from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .student_schema import StudentSchema
    from .student_term_record_schema import StudentTermRecordSchema
    from .yearly_subject_schema import YearlySubjectSchema


class AssessmentSchema(BaseModel):
    """
    This model represents an assessment record for a student including details
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: str | None = None
    student_id: str
    student_term_record_id: str
    yearly_subject_id: str
    total: Optional[float] = None
    rank: Optional[int] = None


class AssessmentRelationshipSchema(BaseModel):
    """This model represents the relationships of a AssessmentSchema."""

    student: Optional[StudentSchema] = None
    student_term_record: Optional[StudentTermRecordSchema] = None
    yearly_subject: Optional[YearlySubjectSchema] = None
