from __future__ import annotations
from pydantic import BaseModel, ConfigDict

from extension.functions.helper import to_camel


class TeacherGradeLinkSchema(BaseModel):
    """
    This model represents the link between a teacher and a grade.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: str | None = None
    teacher_id: str
    grade_id: str
