from __future__ import annotations
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from extension.functions.helper import to_camel


class RegistrationSchema(BaseModel):
    """
    This model represents a registration in the system.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: str | None = None
    student_id: str
    subject_id: str
    semester_id: str
    registration_date: datetime
