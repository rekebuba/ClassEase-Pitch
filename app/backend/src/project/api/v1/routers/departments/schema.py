import uuid
from typing import Optional

from project.schema.schema import BaseSchema


class DepartmentBase(BaseSchema):
    name: str
    code: str
    head_employee_id: Optional[uuid.UUID] = None
