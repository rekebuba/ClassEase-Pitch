from __future__ import annotations
import uuid
from pydantic import BaseModel, ConfigDict

from extension.functions.helper import to_camel


class GradeStreamLinkSchema(BaseModel):
    """
    This model represents the link between a grade and a stream.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID | None = None
    grade_id: uuid.UUID
    stream_id: uuid.UUID
