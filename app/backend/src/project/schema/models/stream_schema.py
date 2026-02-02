from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, ConfigDict

from project.schema.models.grade_schema import GradeWithRelatedSchema
from project.schema.models.student_term_record_schema import (
    StudentTermRecordWithRelatedSchema,
)
from project.schema.models.student_year_record_schema import (
    StudentYearRecordWithRelatedSchema,
)
from project.schema.models.subject_schema import SubjectWithRelatedSchema
from project.utils.utils import to_camel

if TYPE_CHECKING:
    from project.schema.models.grade_schema import GradeSchema
    from project.schema.models.student_term_record_schema import StudentTermRecordSchema
    from project.schema.models.student_year_record_schema import StudentYearRecordSchema
    from project.schema.models.subject_schema import SubjectSchema


class StreamSchema(BaseModel):
    """
    This model represents a stream in the system.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    grade_id: uuid.UUID
    name: str

    @classmethod
    def default_fields(cls) -> set[str]:
        """
        Returns a list of default fields to be used when no specific fields are requested.
        This can be overridden in subclasses if needed.
        """
        return {"id", "name"}


class StreamRelatedSchema(BaseModel):
    """This model represents the relationships of a StreamSchema."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    student_term_records: Optional[List[StudentTermRecordSchema]] = []
    grade: Optional[GradeSchema] = None
    students: Optional[List[StudentYearRecordSchema]] = None
    subjects: Optional[List[SubjectSchema]] = []


class StreamNestedSchema(StreamSchema):
    """This model represents the relationships of a StreamSchema."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    student_term_records: List[StudentTermRecordWithRelatedSchema] = []
    grade: Optional[GradeWithRelatedSchema] = None
    students: List[StudentYearRecordWithRelatedSchema] = []
    subjects: List[SubjectWithRelatedSchema] = []


class StreamWithRelatedSchema(StreamSchema, StreamRelatedSchema):
    pass
