from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List, Optional, Set

from pydantic import AwareDatetime, BaseModel, ConfigDict

from utils.enum import GradeEnum, GradeLevelEnum
from utils.utils import to_camel

if TYPE_CHECKING:
    from .section_schema import SectionSchema, SectionWithRelatedSchema
    from .stream_schema import StreamSchema, StreamWithRelatedSchema
    from .student_schema import StudentSchema, StudentWithRelatedSchema
    from .student_term_record_schema import (
        StudentTermRecordSchema,
    )
    from .subject_schema import SubjectSchema, SubjectWithRelatedSchema
    from .teacher_schema import TeacherSchema, TeacherWithRelatedSchema
    from .year_schema import YearSchema, YearWithRelatedSchema


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

    id: uuid.UUID
    year_id: uuid.UUID
    grade: GradeEnum
    level: GradeLevelEnum
    has_stream: bool
    created_at: AwareDatetime
    updated_at: AwareDatetime

    @classmethod
    def default_fields(cls) -> Set[str]:
        """
        Returns a list of default fields to be used when
        no specific fields are requested.
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
    student_term_records: List[StudentTermRecordSchema]
    teachers: List[TeacherSchema]
    streams: List[StreamSchema]
    students: List[StudentSchema]
    sections: List[SectionSchema]
    subjects: List[SubjectSchema]


class GradeNestedSchema(GradeSchema):
    """This model represents the relationships of a GradeSchema.
    It is used to define the relationships between the GradeSchema and other schemas.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    year: YearWithRelatedSchema
    teachers: List[TeacherWithRelatedSchema]
    streams: List[StreamWithRelatedSchema]
    students: List[StudentWithRelatedSchema]
    sections: List[SectionWithRelatedSchema]
    subjects: List[SubjectWithRelatedSchema]


class GradeWithRelatedSchema(GradeSchema, GradeRelatedSchema):
    pass
