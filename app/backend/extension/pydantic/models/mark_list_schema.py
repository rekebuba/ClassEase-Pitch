from __future__ import annotations
import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict

from extension.enums.enum import MarkListTypeEnum
from extension.functions.helper import to_camel


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
    yearly_subject_id: uuid.UUID
    type: MarkListTypeEnum
    percentage: Optional[float] = None
    score: Optional[float] = None
