import uuid
from typing import Any, List

from pydantic import BaseModel, ConfigDict

from api.v1.routers.employee.schema import TeacherAppliedSubject
from schema.models.grade_schema import GradeSchema
from utils.enum import (
    EmployeeApplicationStatusEnum,
    GenderEnum,
)
from utils.utils import to_camel


class TeacherBasicInfo(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    first_name: str
    father_name: str
    grand_father_name: str
    full_name: str
    gender: GenderEnum
    status: EmployeeApplicationStatusEnum
    subjects: List[TeacherAppliedSubject]
    grades: List[GradeSchema | None]
