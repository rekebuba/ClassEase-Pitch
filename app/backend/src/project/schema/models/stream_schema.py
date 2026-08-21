from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List, Optional

from project.schema.models.grade_schema import GradeWithRelatedSchema
from project.schema.models.student_term_record_schema import (
    StudentTermRecordWithRelatedSchema,
)
from project.schema.models.student_year_record_schema import (
    StudentYearRecordWithRelatedSchema,
)
from project.schema.models.subject_schema import SubjectWithRelatedSchema
from project.schema.schema import BaseSchema

if TYPE_CHECKING:
    from project.schema.models.grade_schema import GradeSchema
    from project.schema.models.student_term_record_schema import StudentTermRecordSchema
    from project.schema.models.student_year_record_schema import StudentYearRecordSchema
    from project.schema.models.subject_schema import SubjectSchema


class StreamSchema(BaseSchema):
    """
    This model represents a stream in the system.
    """

    id: uuid.UUID
    name: str


class StreamRelatedSchema(BaseSchema):
    """This model represents the relationships of a StreamSchema."""

    student_term_records: Optional[List[StudentTermRecordSchema]]
    grade: Optional[GradeSchema]
    students: Optional[List[StudentYearRecordSchema]]
    subjects: Optional[List[SubjectSchema]]


class StreamNestedSchema(StreamSchema):
    """This model represents the relationships of a StreamSchema."""

    student_term_records: List[StudentTermRecordWithRelatedSchema] = []
    grade: Optional[GradeWithRelatedSchema] = None
    students: List[StudentYearRecordWithRelatedSchema] = []
    subjects: List[SubjectWithRelatedSchema] = []


class StreamWithRelatedSchema(StreamSchema, StreamRelatedSchema):
    pass
