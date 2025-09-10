from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING, List

from pydantic import AwareDatetime, BaseModel, ConfigDict

from utils.enum import AcademicTermTypeEnum, AcademicYearStatusEnum
from utils.utils import to_camel

if TYPE_CHECKING:
    from .academic_term_schema import AcademicTermSchema, AcademicTermWithRelatedSchema
    from .event_schema import EventSchema, EventWithRelatedSchema
    from .grade_schema import GradeSchema, GradeWithRelatedSchema
    from .student_schema import StudentSchema, StudentWithRelatedSchema
    from .subject_schema import SubjectSchema, SubjectWithRelatedSchema
    from .teacher_schema import TeacherSchema, TeacherWithRelatedSchema


class YearSchema(BaseModel):
    """
    This model represents a year in the system.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    calendar_type: AcademicTermTypeEnum
    name: str
    start_date: date
    end_date: date
    status: AcademicYearStatusEnum
    created_at: AwareDatetime
    updated_at: AwareDatetime

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

    events: List[EventSchema]
    academic_terms: List[AcademicTermSchema]
    grades: List[GradeSchema]
    students: List[StudentSchema]
    teachers: List[TeacherSchema]
    subjects: List[SubjectSchema]


class YearNestedSchema(YearSchema):
    """This model represents the relationships of a YearSchema."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    events: List[EventWithRelatedSchema]
    academic_terms: List[AcademicTermWithRelatedSchema]
    grades: List[GradeWithRelatedSchema]
    students: List[StudentWithRelatedSchema]
    teachers: List[TeacherWithRelatedSchema]
    subjects: List[SubjectWithRelatedSchema]


class YearWithRelatedSchema(YearSchema, YearRelatedSchema):
    """This model represents a YearSchema with its relationships."""

    pass
