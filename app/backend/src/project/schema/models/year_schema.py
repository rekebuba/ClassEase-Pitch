from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING, List

from pydantic import AwareDatetime

from project.schema.schema import BaseSchema
from project.utils.enum import AcademicTermTypeEnum, AcademicYearStatusEnum

if TYPE_CHECKING:
    from project.schema.models.academic_term_schema import (
        AcademicTermSchema,
        AcademicTermWithRelatedSchema,
    )
    from project.schema.models.event_schema import EventSchema, EventWithRelatedSchema
    from project.schema.models.grade_schema import GradeWithRelatedSchema
    from project.schema.models.student_schema import (
        StudentWithRelatedSchema,
    )
    from project.schema.models.subject_schema import (
        SubjectWithRelatedSchema,
    )


class YearSchema(BaseSchema):
    """
    This model represents a year in the system.
    """

    id: uuid.UUID
    calendar_type: AcademicTermTypeEnum
    name: str
    start_date: date
    end_date: date
    status: AcademicYearStatusEnum
    created_at: AwareDatetime
    updated_at: AwareDatetime


class YearRelatedSchema(BaseSchema):
    """This model represents the relationships of a YearSchema."""

    events: List[EventSchema]
    academic_terms: List[AcademicTermSchema]


class YearNestedSchema(YearSchema):
    """This model represents the relationships of a YearSchema."""

    events: List[EventWithRelatedSchema]
    academic_terms: List[AcademicTermWithRelatedSchema]
    grades: List[GradeWithRelatedSchema]
    students: List[StudentWithRelatedSchema]
    subjects: List[SubjectWithRelatedSchema]


class YearWithRelatedSchema(YearSchema, YearRelatedSchema):
    """This model represents a YearSchema with its relationships."""

    pass
