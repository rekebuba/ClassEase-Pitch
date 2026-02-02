from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict

from project.utils.utils import to_camel

if TYPE_CHECKING:
    from project.schema.models.grade_schema import GradeSchema
    from project.schema.models.stream_schema import StreamSchema
    from project.schema.models.subject_schema import SubjectSchema


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
