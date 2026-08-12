from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING

from pydantic import AwareDatetime

from project.schema.schema import BaseSchema
from project.utils.enum import EmploymentTypeEnum

if TYPE_CHECKING:
    from project.schema.models.position_schema import PositionSchema


class JobSchema(BaseSchema):
    id: uuid.UUID
    position: PositionSchema
    school_id: uuid.UUID
    description: str
    employment_type: EmploymentTypeEnum
    application_deadline: date | None
    openings_count: int
    allow_applications: bool
    created_at: AwareDatetime
    updated_at: AwareDatetime
