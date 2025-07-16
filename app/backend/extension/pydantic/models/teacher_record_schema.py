from __future__ import annotations
import uuid
from typing import TYPE_CHECKING, Optional, List
from pydantic import BaseModel, ConfigDict

from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .teacher_schema import TeacherSchema
    from .academic_term_schema import AcademicTermSchema
    from .yearly_subject_schema import YearlySubjectSchema
    from .section_schema import SectionSchema


class TeacherRecordSchema(BaseModel):
    """
    This model represents the record of teachers, including their associated subjects, grades, and sections.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID | None = None
    teacher_id: uuid.UUID
    academic_term_id: uuid.UUID


class TeacherRecordRelationshipSchema(BaseModel):
    """This model represents the relationships of a TeacherRecordSchema."""

    teacher: Optional[TeacherSchema] = None
    academic_term: Optional[AcademicTermSchema] = None
    yearly_subjects_link: Optional[List[YearlySubjectSchema]] = None
    sections_link: Optional[List[SectionSchema]] = None
