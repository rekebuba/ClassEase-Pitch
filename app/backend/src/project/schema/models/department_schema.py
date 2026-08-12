import uuid
from typing import Optional

from pydantic import AwareDatetime

from project.schema.schema import BaseSchema


class DepartmentSchema(BaseSchema):
    id: uuid.UUID
    name: str
    code: str
    head_employee_id: Optional[uuid.UUID] = None
    created_at: AwareDatetime
    updated_at: AwareDatetime
