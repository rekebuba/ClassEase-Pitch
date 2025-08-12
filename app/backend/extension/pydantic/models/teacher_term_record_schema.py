from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import uuid
from pydantic import BaseModel, ConfigDict
from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .academic_term_schema import AcademicTermSchema
    from .grade_schema import GradeSchema
    from .section_schema import SectionSchema
    from .stream_schema import StreamSchema
    from .subject_schema import SubjectSchema
    from .teacher_schema import TeacherSchema


class TeacherTermRecordSchema(BaseModel):
    """"""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    teacher_id: uuid.UUID
    academic_term_id: uuid.UUID
    subject_id: uuid.UUID
    grade_id: uuid.UUID
    section_id: uuid.UUID
    stream_id: uuid.UUID | None


class TeacherTermRecordRelatedSchema(BaseModel):
    """
    This model represents a TeacherTermRecordSchema with its relationships.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    teacher: Optional[TeacherSchema] = None
    academic_term: Optional[AcademicTermSchema] = None
    subject: Optional[SubjectSchema] = None
    section: Optional[SectionSchema] = None
    grade: Optional[GradeSchema] = None
    stream: Optional[StreamSchema] = None


class TeacherTermRecordWithRelatedSchema(
    TeacherTermRecordSchema, TeacherTermRecordRelatedSchema
):
    """
    This model combines the TeacherTermRecordSchema with its relationships.
    It is used to provide a complete view of a teacher's term record along with related entities.
    """

    pass
