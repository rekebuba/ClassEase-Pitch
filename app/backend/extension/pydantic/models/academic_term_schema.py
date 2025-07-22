from __future__ import annotations
import uuid
from typing import TYPE_CHECKING, Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import date

from extension.enums.enum import AcademicTermEnum
from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .year_schema import YearSchema
    from .student_term_record_schema import StudentTermRecordSchema
    from .teacher_record_schema import TeacherRecordSchema


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


class AcademicTermRelationshipSchema(BaseModel):
    """This model represents the relationships of a AcademicTermSchema."""

    year: Optional[YearSchema] = None
    student_term_records: Optional[List[StudentTermRecordSchema]] = None
    teacher_records: Optional[List[TeacherRecordSchema]] = None
