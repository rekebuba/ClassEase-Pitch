from __future__ import annotations
import uuid
from typing import TYPE_CHECKING, Optional, List
from pydantic import BaseModel, ConfigDict

from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .student_schema import StudentSchema
    from .student_year_record_schema import StudentYearRecordSchema
    from .academic_term_schema import AcademicTermSchema
    from .section_schema import SectionSchema
    from .assessment_schema import AssessmentSchema


class StudentTermRecordSchema(BaseModel):
    """
    This model represents the average result of a student for a particular term and year.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID | None = None
    student_id: uuid.UUID
    academic_term_id: uuid.UUID
    section_id: uuid.UUID
    student_year_record_id: Optional[uuid.UUID] = None
    average: Optional[float] = None
    rank: Optional[int] = None


class StudentTermRecordRelationshipSchema(BaseModel):
    """This model represents the relationships of a StudentTermRecordSchema."""

    student: Optional[StudentSchema] = None
    student_year_record: Optional[StudentYearRecordSchema] = None
    academic_term: Optional[AcademicTermSchema] = None
    section: Optional[SectionSchema] = None
    assessments: Optional[List[AssessmentSchema]] = None
