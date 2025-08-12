from __future__ import annotations
import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, List
from pydantic import BaseModel, ConfigDict

from extension.enums.enum import AcademicTermTypeEnum, AcademicYearStatusEnum
from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .academic_term_schema import AcademicTermWithRelatedSchema
    from .event_schema import EventWithRelatedSchema
    from .grade_schema import GradeWithRelatedSchema
    from .student_schema import StudentWithRelatedSchema
    from .student_year_record_schema import StudentYearRecordWithRelatedSchema
    from .subject_schema import SubjectWithRelatedSchema
    from .teacher_schema import TeacherWithRelatedSchema
    from .student_year_record_schema import StudentYearRecordSchema
    from .event_schema import EventSchema
    from .academic_term_schema import AcademicTermSchema
    from .yearly_subject_schema import YearlySubjectSchema
    from .grade_schema import GradeSchema
    from .section_schema import SectionSchema
    from .stream_schema import StreamSchema
    from .student_schema import StudentSchema
    from .subject_schema import SubjectSchema
    from .teacher_schema import TeacherSchema


class YearSchema(BaseModel):
    """
    This model represents a year in the system.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID | None = None
    calendar_type: AcademicTermTypeEnum
    name: str
    start_date: date
    end_date: date
    status: AcademicYearStatusEnum
    created_at: datetime
    updated_at: datetime

    @classmethod
    def default_fields(cls) -> set[str]:
        """
        Returns a list of default fields to be used when no specific fields are requested.
        This can be overridden in subclasses if needed.
        """
        return {"id", "name", "status"}


class YearRelatedSchema(BaseModel):
    """This model represents the relationships of a YearSchema."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    student_year_records: List[StudentYearRecordSchema] = []
    events: List[EventSchema] = []
    academic_terms: List[AcademicTermSchema] = []
    yearly_subjects: List[YearlySubjectSchema] = []
    grades: List[GradeSchema] = []
    students: List[StudentSchema] = []
    teachers: List[TeacherSchema] = []
    subjects: List[SubjectSchema] = []


class YearNestedSchema(YearSchema):
    """This model represents the relationships of a YearSchema."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    student_year_records: List[StudentYearRecordWithRelatedSchema] = []
    events: List[EventWithRelatedSchema] = []
    academic_terms: List[AcademicTermWithRelatedSchema] = []
    grades: List[GradeWithRelatedSchema] = []
    students: List[StudentWithRelatedSchema] = []
    teachers: List[TeacherWithRelatedSchema] = []
    subjects: List[SubjectWithRelatedSchema] = []


class YearWithRelatedSchema(YearSchema, YearRelatedSchema):
    """This model represents a YearSchema with its relationships."""

    pass
