from __future__ import annotations
import uuid
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

    id: uuid.UUID | None = None
    student_id: uuid.UUID
    subject_id: uuid.UUID
    semester_id: uuid.UUID
    registration_date: datetime
