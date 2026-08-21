from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING, List, Optional

from project.schema.schema import BaseSchema
from project.utils.enum import AcademicTermEnum

if TYPE_CHECKING:
    from project.schema.models.student_term_record_schema import StudentTermRecordSchema
    from project.schema.models.year_schema import YearSchema


class AcademicTermSchema(BaseSchema):
    """
    This model represents an academic term in the system.
    """

    id: uuid.UUID
    year_id: uuid.UUID
    name: AcademicTermEnum
    start_date: date
    end_date: date
    registration_start: Optional[date]
    registration_end: Optional[date]

    @classmethod
    def default_fields(cls) -> set[str]:
        """
        Returns a list of default fields to be used
        when no specific fields are requested.
        This can be overridden in subclasses if needed.
        """
        return {"id", "name", "start_date", "end_date"}


class AcademicTermRelatedSchema(BaseSchema):
    """This model represents the relationships of a AcademicTermSchema."""

    year: Optional[YearSchema] = None
    student_term_records: Optional[List[StudentTermRecordSchema]] = []


class AcademicTermWithRelatedSchema(AcademicTermSchema, AcademicTermRelatedSchema):
    """This model represents an AcademicTermSchema with its relationships."""

    pass
