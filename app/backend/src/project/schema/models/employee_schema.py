from __future__ import annotations

import uuid
from datetime import date
from typing import Optional

from pydantic import AwareDatetime

from project.schema.models import UserSchema
from project.schema.schema import BaseSchema
from project.utils.enum import EmploymentStatusEnum, EmploymentTypeEnum


class EmployeeSchema(BaseSchema):
    id: uuid.UUID
    user: UserSchema
    employee_number: str
    employment_status: EmploymentStatusEnum
    employment_type: EmploymentTypeEnum
    hire_date: date
    termination_date: Optional[date]
    manager_employee_id: Optional[uuid.UUID]
    work_email: Optional[str]
    work_phone: Optional[str]
    created_at: AwareDatetime
    updated_at: AwareDatetime
