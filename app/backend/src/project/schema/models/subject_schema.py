from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List

from pydantic import AwareDatetime

from project.schema.schema import BaseSchema

if TYPE_CHECKING:
    from project.schema.models.grade_schema import GradeSchema, GradeWithRelatedSchema
    from project.schema.models.mark_list_schema import MarkListSchema
    from project.schema.models.stream_schema import (
        StreamSchema,
        StreamWithRelatedSchema,
    )
    from project.schema.models.student_schema import StudentSchema
    from project.schema.models.teacher_schema import (
        TeacherSchema,
        TeacherWithRelatedSchema,
    )
    from project.schema.models.year_schema import YearSchema


class BasicSubjectSchema(BaseSchema):
    """
    This model represents a basic subject in the system. It inherits from BaseModel.
    """

    id: uuid.UUID
    name: str
    code: str


class SubjectSchema(BaseSchema):
    """
    This model represents a subject in the system. It inherits from BaseModel.
    """

    id: uuid.UUID
    year_id: uuid.UUID
    name: str
    code: str
    created_at: AwareDatetime
    updated_at: AwareDatetime


class SubjectRelatedSchema(BaseSchema):
    """This model represents the relationships of a SubjectSchema.
    It is used to define the relationships between the SubjectSchema and other schemas.
    """

    year: YearSchema
    teachers: List[TeacherSchema]
    students: List[StudentSchema]
    mark_lists: List[MarkListSchema]
    streams: List[StreamSchema]
    grades: List[GradeSchema]


class SubjectNestedSchema(SubjectSchema):
    """This model represents the relationships of a SubjectSchema.
    It is used to define the relationships between the SubjectSchema and other schemas.
    """

    teachers: List[TeacherWithRelatedSchema]
    streams: List[StreamWithRelatedSchema]
    grades: List[GradeWithRelatedSchema]


class SubjectWithRelatedSchema(SubjectSchema, SubjectRelatedSchema):
    pass
