from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List

from pydantic import AwareDatetime

from project.schema.schema import BaseSchema
from project.utils.enum import GradeEnum, GradeLevelEnum

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
    from project.schema.models.subject_schema import (
        SubjectSchema,
    )
    from project.schema.models.teacher_schema import (
        TeacherWithRelatedSchema,
    )
    from project.schema.models.year_schema import YearWithRelatedSchema


class GradeSchema(BaseSchema):
    """
    This model represents a grade in the system. It inherits from BaseModel.
    """

    id: uuid.UUID
    school_id: uuid.UUID
    grade: GradeEnum
    level: GradeLevelEnum
    has_stream: bool
    created_at: AwareDatetime
    updated_at: AwareDatetime


class GradeWithSubjectSchema(GradeSchema):
    """
    This model represents a grade along with its associated subjects."""

    subjects: List[SubjectSchema]


class GradeRelatedSchema(BaseSchema):
    """This model represents the relationships of a GradeSchema.
    It is used to define the relationships between the GradeSchema and other schemas.
    """

    streams: List[StreamSchema]
    students: List[StudentSchema]
    sections: List[SectionSchema]
    subjects: List[SubjectSchema]


class GradeNestedSchema(GradeSchema):
    """This model represents the relationships of a GradeSchema.
    It is used to define the relationships between the GradeSchema and other schemas.
    """

    year: YearWithRelatedSchema
    teachers: List[TeacherWithRelatedSchema]
    streams: List[StreamWithRelatedSchema]
    students: List[StudentWithRelatedSchema]
    sections: List[SectionWithRelatedSchema]


class GradeWithRelatedSchema(GradeSchema, GradeRelatedSchema):
    pass
