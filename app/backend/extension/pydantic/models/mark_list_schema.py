from __future__ import annotations
import uuid
from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, ConfigDict

from extension.enums.enum import MarkListTypeEnum
from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from extension.pydantic.models.academic_term_schema import AcademicTermSchema
    from extension.pydantic.models.student_schema import StudentSchema
    from extension.pydantic.models.subject_schema import SubjectSchema


class MarkListSchema(BaseModel):
    """
    This model represents an assessment record for a student including details
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID | None = None
    student_id: uuid.UUID
    academic_term_id: uuid.UUID
    subject_id: uuid.UUID
    type: MarkListTypeEnum
    percentage: Optional[float] = None
    score: Optional[float] = None


class MarkListRelationshipSchema(BaseModel):
    """
    This model represents the relationships associated with a MarkList.
    """

    academic_term: Optional[AcademicTermSchema] = None
    subject: Optional[SubjectSchema] = None
    student: Optional[StudentSchema] = None
