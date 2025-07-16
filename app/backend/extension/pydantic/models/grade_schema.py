from __future__ import annotations
import uuid
from typing import TYPE_CHECKING, List, Set
from pydantic import BaseModel, ConfigDict, Field

from extension.enums.enum import GradeLevelEnum
from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .teacher_schema import TeacherSchema
    from .stream_schema import StreamSchema
    from .yearly_subject_schema import YearlySubjectSchema
    from .student_year_record_schema import StudentYearRecordSchema
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


class GradeRelationshipSchema(BaseModel):
    """This model represents the relationships of a GradeSchema.
    It is used to define the relationships between the GradeSchema and other schemas.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    year: YearSchema
    teachers: List[TeacherSchema] = []
    streams: List[StreamSchema] = []
    yearly_subjects: List[YearlySubjectSchema] = Field(alias="subjects")
    student_year_records: List[StudentYearRecordSchema] = []
    students: List[StudentSchema] = []
    sections_link: List[SectionSchema] = Field(alias="sections")
    subject_links: List[SubjectSchema] = Field(alias="subjects")


class GradeWithRelationshipsSchema(GradeSchema, GradeRelationshipSchema):
    pass
