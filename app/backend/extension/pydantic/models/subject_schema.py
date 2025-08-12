from __future__ import annotations
import uuid
from typing import TYPE_CHECKING, List, Optional
from pydantic import BaseModel, ConfigDict
from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .stream_schema import StreamWithRelatedSchema
    from .teacher_schema import TeacherWithRelatedSchema
    from .teacher_term_record_schema import TeacherTermRecordWithRelatedSchema
    from .grade_schema import GradeWithRelatedSchema
    from .teacher_term_record_schema import TeacherTermRecordSchema
    from .teacher_schema import TeacherSchema
    from .grade_schema import GradeSchema
    from .stream_schema import StreamSchema


class SubjectSchema(BaseModel):
    """
    This model represents a subject in the system. It inherits from BaseModel.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID | None = None
    year_id: uuid.UUID
    name: str
    code: str

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

    teacher_term_records: Optional[List[TeacherTermRecordSchema]] = []
    teachers: List[TeacherSchema] = []
    streams: List[StreamSchema] = []
    grades: List[GradeSchema] = []


class SubjectNestedSchema(SubjectSchema):
    """This model represents the relationships of a SubjectSchema.
    It is used to define the relationships between the SubjectSchema and other schemas.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    teacher_term_records: Optional[List[TeacherTermRecordWithRelatedSchema]] = []
    teachers: List[TeacherWithRelatedSchema] = []
    streams: List[StreamWithRelatedSchema] = []
    grades: List[GradeWithRelatedSchema] = []


class SubjectWithRelatedSchema(SubjectSchema, SubjectRelatedSchema):
    pass
