from __future__ import annotations

import uuid

from project.schema.schema import BaseSchema


class GradeStreamLinkSchema(BaseSchema):
    """
    This model represents the link between a grade and a stream.
    """

    id: uuid.UUID | None = None
    grade_id: uuid.UUID
    stream_id: uuid.UUID
