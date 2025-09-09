from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, ConfigDict

from extension.enums.enum import AcademicTermEnum
from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .student_term_record_schema import StudentTermRecordSchema
    from .teacher_record_schema import TeacherRecordSchema
    from .teacher_term_record_schema import TeacherTermRecordSchema
    from .year_schema import YearSchema


class AcademicTermSchema(BaseModel):
    """
    This model represents an academic term in the system.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID | None = None
    year_id: uuid.UUID
    name: AcademicTermEnum
    start_date: date
    end_date: date
    registration_start: Optional[date] = None
    registration_end: Optional[date] = None

    @classmethod
    def default_fields(cls) -> set[str]:
        """
        Returns a list of default fields to be used when no specific fields are requested.
        This can be overridden in subclasses if needed.
        """
        return {"id", "name", "start_date", "end_date"}


class AcademicTermRelatedSchema(BaseModel):
    """This model represents the relationships of a AcademicTermSchema."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    year: Optional[YearSchema] = None
    teacher_term_records: Optional[List[TeacherTermRecordSchema]] = []
    student_term_records: Optional[List[StudentTermRecordSchema]] = []
    teacher_records: Optional[List[TeacherRecordSchema]] = []


class AcademicTermWithRelatedSchema(AcademicTermSchema, AcademicTermRelatedSchema):
    """This model represents an AcademicTermSchema with its relationships."""

    pass
