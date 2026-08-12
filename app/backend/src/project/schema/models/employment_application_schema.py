from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from pydantic import AwareDatetime

from project.schema.schema import BaseSchema
from project.utils.enum import EmploymentApplicationStatusEnum

if TYPE_CHECKING:
    from project.schema.models import JobSchema, UserSchema


class EmploymentApplicationSchema(BaseSchema):
    id: uuid.UUID
    applicant_user: UserSchema
    job_posting: JobSchema
    cover_note: str | None
    reviewer_note: str | None
    status: EmploymentApplicationStatusEnum
    submitted_at: AwareDatetime
    reviewed_at: AwareDatetime
    created_at: AwareDatetime
    updated_at: AwareDatetime
