from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, ConfigDict

from project.utils.utils import to_camel

if TYPE_CHECKING:
    from project.schema.models.academic_term_schema import AcademicTermSchema
    from project.schema.models.section_schema import SectionSchema
    from project.schema.models.teacher_schema import TeacherSchema
    from project.schema.models.yearly_subject_schema import YearlySubjectSchema


class TeacherRecordSchema(BaseModel):
    """
    This model represents the record of
    teachers, including their associated subjects, grades, and sections.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID | None = None
    teacher_id: uuid.UUID
    academic_term_id: uuid.UUID


class TeacherRecordRelatedSchema(BaseModel):
    """This model represents the relationships of a TeacherRecordSchema."""

    teacher: Optional[TeacherSchema] = None
    academic_term: Optional[AcademicTermSchema] = None
    yearly_subjects_link: Optional[List[YearlySubjectSchema]] = None
    sections_link: Optional[List[SectionSchema]] = None
