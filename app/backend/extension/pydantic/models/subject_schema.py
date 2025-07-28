from __future__ import annotations
import uuid
from typing import TYPE_CHECKING, List, Optional
from pydantic import BaseModel, ConfigDict
from extension.functions.helper import to_camel

if TYPE_CHECKING:
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
    name: str
    code: str

    @classmethod
    def default_fields(cls) -> set[str]:
        """
        Returns a list of default fields to be used when no specific fields are requested.
        This can be overridden in subclasses if needed.
        """
        return {"id", "name", "code"}


class SubjectRelationshipSchema(BaseModel):
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
    grades: List[GradeSchema] = []
    streams: List[StreamSchema] = []


class SubjectWithRelationshipsSchema(SubjectSchema, SubjectRelationshipSchema):
    pass
