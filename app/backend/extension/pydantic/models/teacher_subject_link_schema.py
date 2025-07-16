from __future__ import annotations
import uuid
from pydantic import BaseModel, ConfigDict

from extension.functions.helper import to_camel


class TeacherSubjectLinkSchema(BaseModel):
    """
    This model represents the link between a teacher and a subject.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID | None = None
    teacher_id: uuid.UUID
    subject_id: uuid.UUID
