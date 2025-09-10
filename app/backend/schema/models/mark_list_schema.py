from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict

from utils.enum import MarkListTypeEnum
from utils.utils import to_camel

if TYPE_CHECKING:
    from .student_schema import StudentSchema
    from .student_term_record_schema import StudentTermRecordSchema
    from .subject_schema import SubjectSchema


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
    student_term_record_id: uuid.UUID
    subject_id: uuid.UUID
    type: MarkListTypeEnum
    percentage: Optional[float] = None
    score: Optional[float] = None


class MarkListRelatedSchema(BaseModel):
    """
    This model represents the relationships associated with a MarkList.
    """

    student_term_record: Optional[StudentTermRecordSchema] = None
    subject: Optional[SubjectSchema] = None
    student: Optional[StudentSchema] = None
