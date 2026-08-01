from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Optional

from project.schema.schema import BaseSchema

if TYPE_CHECKING:
    from project.schema.models.student_schema import StudentSchema
    from project.schema.models.student_term_record_schema import StudentTermRecordSchema
    from project.schema.models.subject_offering_schema import SubjectOfferingSchema


class AssessmentSchema(BaseSchema):
    """
    This model represents an assessment record for a student including details
    """

    id: uuid.UUID | None = None
    student_id: uuid.UUID
    student_term_record_id: uuid.UUID
    subject_offering_id: uuid.UUID
    total: Optional[float] = None
    rank: Optional[int] = None


class AssessmentRelatedSchema(BaseSchema):
    """This model represents the relationships of a AssessmentSchema."""

    student: Optional[StudentSchema] = None
    student_term_record: Optional[StudentTermRecordSchema] = None
    subject_offering: Optional[SubjectOfferingSchema] = None
