from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List, Optional

from pydantic import AwareDatetime, BaseModel, ConfigDict

from project.utils.enum import GradeEnum, GradeLevelEnum
from project.utils.utils import to_camel

if TYPE_CHECKING:
    from project.schema.models.section_schema import (
        SectionSchema,
        SectionWithRelatedSchema,
    )
    from project.schema.models.stream_schema import (
        StreamSchema,
        StreamWithRelatedSchema,
    )
    from project.schema.models.student_schema import (
        StudentSchema,
        StudentWithRelatedSchema,
    )
    from project.schema.models.student_term_record_schema import (
        StudentTermRecordSchema,
    )
    from project.schema.models.subject_schema import (
        SubjectSchema,
    )
    from project.schema.models.teacher_schema import (
        TeacherWithRelatedSchema,
    )
    from project.schema.models.year_schema import YearSchema, YearWithRelatedSchema


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


class GradeWithSubjectSchema(GradeSchema):
    """
    This model represents a grade along with its associated subjects."""

    subjects: List[SubjectSchema]


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


class GradeWithRelatedSchema(GradeSchema, GradeRelatedSchema):
    pass
