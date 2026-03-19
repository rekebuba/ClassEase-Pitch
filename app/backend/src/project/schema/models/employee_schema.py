from __future__ import annotations

import uuid

from pydantic import BaseModel


class EmployeeSchema(BaseModel):
    id: uuid.UUID
    first_name: str
