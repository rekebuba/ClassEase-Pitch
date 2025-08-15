from __future__ import annotations
import uuid
from typing import TYPE_CHECKING, Optional, List
from pydantic import BaseModel, ConfigDict, Field

from extension.functions.helper import to_camel
from extension.pydantic.models.grade_schema import GradeWithRelatedSchema
from extension.pydantic.models.student_term_record_schema import (
    StudentTermRecordWithRelatedSchema,
)
from extension.pydantic.models.student_year_record_schema import (
    StudentYearRecordWithRelatedSchema,
)
from extension.pydantic.models.subject_schema import SubjectWithRelatedSchema
from extension.pydantic.models.teacher_term_record_schema import (
    TeacherTermRecordWithRelatedSchema,
)

if TYPE_CHECKING:
    from .grade_stream_subject_schema import GradeStreamSubjectSchema
    from .student_term_record_schema import StudentTermRecordSchema
    from .teacher_term_record_schema import TeacherTermRecordSchema
    from .grade_schema import GradeSchema
    from .yearly_subject_schema import YearlySubjectSchema
    from .student_year_record_schema import StudentYearRecordSchema
    from .subject_schema import SubjectSchema


class StreamSchema(BaseModel):
    """
    This model represents a stream in the system.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID | None = None
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

    teacher_term_records: Optional[List[TeacherTermRecordSchema]] = []
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

    teacher_term_records: List[TeacherTermRecordWithRelatedSchema] = []
    student_term_records: List[StudentTermRecordWithRelatedSchema] = []
    grade: Optional[GradeWithRelatedSchema] = None
    students: List[StudentYearRecordWithRelatedSchema] = []
    subjects: List[SubjectWithRelatedSchema] = []


class StreamWithRelatedSchema(StreamSchema, StreamRelatedSchema):
    pass
