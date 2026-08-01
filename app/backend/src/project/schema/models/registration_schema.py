from __future__ import annotations

import uuid
from datetime import datetime

from project.schema.schema import BaseSchema


class RegistrationSchema(BaseSchema):
    """
    This model represents a registration in the system.
    """

    id: uuid.UUID | None = None
    student_id: uuid.UUID
    subject_id: uuid.UUID
    semester_id: uuid.UUID
    registration_date: datetime
