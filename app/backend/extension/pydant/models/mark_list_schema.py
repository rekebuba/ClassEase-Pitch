from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict

from extension.enums.enum import MarkListTypeEnum
from extension.functions.helper import to_camel


class MarkListSchema(BaseModel):
    """
    This model represents a list of marks for students in various assessments.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    student_id: str
    academic_term_id: str
    yearly_subject_id: str
    type: MarkListTypeEnum
    percentage: int
    score: Optional[float] = None
