from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict

from utils.utils import to_camel

if TYPE_CHECKING:
    from .grade_schema import GradeSchema
    from .stream_schema import StreamSchema
    from .subject_schema import SubjectSchema


class GradeStreamSubjectSchema(BaseModel):
    """
    This model represents the relationship between a Grade and a Stream Subject.
    It inherits from BaseModel.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    grade: GradeSchema
    subject: SubjectSchema
    stream: Optional[StreamSchema]
