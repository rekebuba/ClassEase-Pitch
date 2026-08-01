from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Optional

from project.schema.schema import BaseSchema

if TYPE_CHECKING:
    from project.schema.models.student_schema import StudentSchema
    from project.schema.models.student_year_record_schema import StudentYearRecordSchema
    from project.schema.models.subject_offering_schema import SubjectOfferingSchema


class SubjectYearlyAverageSchema(BaseSchema):
    """
    This model represents the yearly average of a subject for a student.
    """

    id: uuid.UUID | None = None
    student_id: uuid.UUID
    subject_offering_id: uuid.UUID
    student_year_record_id: Optional[uuid.UUID] = None
    average: Optional[float] = None
    rank: Optional[int] = None


class SubjectYearlyAverageRelatedSchema(BaseSchema):
    """This model represents the relationships of a SubjectYearlyAverageSchema."""

    student: Optional[StudentSchema] = None
    subject_offering: Optional[SubjectOfferingSchema] = None
    student_year_record: Optional[StudentYearRecordSchema] = None
