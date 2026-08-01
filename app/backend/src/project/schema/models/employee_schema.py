from __future__ import annotations

import uuid
from datetime import date
from typing import Optional

from project.schema.schema import BaseSchema
from project.utils.enum import EmploymentStatusEnum, EmploymentTypeEnum


class EmployeeSchema(BaseSchema):
    id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    employee_number: str
    employment_status: EmploymentStatusEnum
    employment_type: EmploymentTypeEnum
    hire_date: date
    termination_date: Optional[date] = None
