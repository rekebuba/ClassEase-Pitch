from __future__ import annotations

import uuid

from pydantic import BaseModel, ConfigDict

from utils.utils import to_camel


class TeacherGradeLinkSchema(BaseModel):
    """
    This model represents the link between a teacher and a grade.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID | None = None
    teacher_id: uuid.UUID
    grade_id: uuid.UUID
