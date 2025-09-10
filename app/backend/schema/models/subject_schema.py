from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List, Optional

from pydantic import AwareDatetime, BaseModel, ConfigDict

from utils.utils import to_camel

if TYPE_CHECKING:
    from schema.models.mark_list_schema import MarkListSchema
    from schema.models.student_schema import StudentSchema
    from schema.models.year_schema import YearSchema

    from .grade_schema import GradeSchema, GradeWithRelatedSchema
    from .stream_schema import StreamSchema, StreamWithRelatedSchema
    from .teacher_schema import TeacherSchema, TeacherWithRelatedSchema
    from .teacher_term_record_schema import (
        TeacherTermRecordSchema,
        TeacherTermRecordWithRelatedSchema,
    )


class SubjectSchema(BaseModel):
    """
    This model represents a subject in the system. It inherits from BaseModel.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    year_id: uuid.UUID
    name: str
    code: str
    created_at: AwareDatetime
    updated_at: AwareDatetime

    @classmethod
    def default_fields(cls) -> set[str]:
        """
        Returns a list of default fields to be used when no specific fields are requested.
        This can be overridden in subclasses if needed.
        """
        return {"id", "name", "code"}


class SubjectRelatedSchema(BaseModel):
    """This model represents the relationships of a SubjectSchema.
    It is used to define the relationships between the SubjectSchema and other schemas.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    year: YearSchema
    teacher_term_records: Optional[List[TeacherTermRecordSchema]]
    teachers: List[TeacherSchema]
    students: List[StudentSchema]
    mark_lists: List[MarkListSchema]
    streams: List[StreamSchema]
    grades: List[GradeSchema]


class SubjectNestedSchema(SubjectSchema):
    """This model represents the relationships of a SubjectSchema.
    It is used to define the relationships between the SubjectSchema and other schemas.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    teacher_term_records: List[TeacherTermRecordWithRelatedSchema]
    teachers: List[TeacherWithRelatedSchema]
    streams: List[StreamWithRelatedSchema]
    grades: List[GradeWithRelatedSchema]


class SubjectWithRelatedSchema(SubjectSchema, SubjectRelatedSchema):
    pass
