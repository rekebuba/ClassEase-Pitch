from __future__ import annotations
import uuid
from typing import TYPE_CHECKING, List, Optional, Set
from pydantic import BaseModel, ConfigDict

from extension.enums.enum import GradeLevelEnum
from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .grade_stream_subject_schema import GradeStreamSubjectSchema
    from .section_schema import SectionWithRelatedSchema
    from .stream_schema import StreamWithRelatedSchema
    from .student_schema import StudentWithRelatedSchema
    from .student_term_record_schema import StudentTermRecordWithRelatedSchema
    from .subject_schema import SubjectWithRelatedSchema
    from .teacher_schema import TeacherWithRelatedSchema
    from .teacher_term_record_schema import TeacherTermRecordWithRelatedSchema
    from .year_schema import YearWithRelatedSchema
    from .student_term_record_schema import StudentTermRecordSchema
    from .teacher_term_record_schema import TeacherTermRecordSchema
    from .teacher_schema import TeacherSchema
    from .stream_schema import StreamSchema
    from .student_schema import StudentSchema
    from .year_schema import YearSchema
    from .section_schema import SectionSchema
    from .subject_schema import SubjectSchema


class GradeSchema(BaseModel):
    """
    This model represents a grade in the system. It inherits from BaseModel.
    """

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID | None = None
    year_id: uuid.UUID
    grade: str
    level: GradeLevelEnum
    has_stream: bool = False

    @classmethod
    def default_fields(cls) -> Set[str]:
        """
        Returns a list of default fields to be used when no specific fields are requested.
        This can be overridden in subclasses if needed.
        """
        return {"id", "grade"}


class GradeRelatedSchema(BaseModel):
    """This model represents the relationships of a GradeSchema.
    It is used to define the relationships between the GradeSchema and other schemas.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    year: Optional[YearSchema]
    teacher_term_records: Optional[List[TeacherTermRecordSchema]] = []
    student_term_records: Optional[List[StudentTermRecordSchema]] = []
    teachers: List[TeacherSchema] = []
    streams: List[StreamSchema] = []
    students: List[StudentSchema] = []
    sections: List[SectionSchema] = []
    subjects: List[SubjectSchema] = []


class GradeNestedSchema(GradeSchema):
    """This model represents the relationships of a GradeSchema.
    It is used to define the relationships between the GradeSchema and other schemas.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    year: Optional[YearWithRelatedSchema]
    teacher_term_records: Optional[List[TeacherTermRecordWithRelatedSchema]] = []
    student_term_records: Optional[List[StudentTermRecordWithRelatedSchema]] = []
    teachers: List[TeacherWithRelatedSchema] = []
    streams: List[StreamWithRelatedSchema] = []
    students: List[StudentWithRelatedSchema] = []
    sections: List[SectionWithRelatedSchema] = []
    subjects: List[SubjectWithRelatedSchema] = []


class GradeWithRelatedSchema(GradeSchema, GradeRelatedSchema):
    pass
