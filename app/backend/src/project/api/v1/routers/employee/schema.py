import uuid
from datetime import date
from typing import List, Optional

from pydantic import AwareDatetime, BaseModel, ConfigDict
from pydantic_extra_types.phone_numbers import PhoneNumber

from project.schema.models.subject_schema import BasicSubjectSchema
from project.utils.enum import (
    EmployeeApplicationStatusEnum,
    EmployeePositionEnum,
    ExperienceYearEnum,
    GenderEnum,
    HighestEducationEnum,
)
from project.utils.utils import to_camel


class EmployeeBasicInfo(BaseModel):
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
    date_of_birth: date
    gender: GenderEnum
    nationality: str
    social_security_number: str
    address: str
    city: str
    state: str
    country: str
    emergency_contact_name: str
    emergency_contact_relation: str
    emergency_contact_phone: PhoneNumber
    highest_education: HighestEducationEnum
    university: str
    graduation_year: int
    gpa: float
    position: EmployeePositionEnum
    years_of_experience: ExperienceYearEnum
    secondary_phone: Optional[str]
    resume: Optional[str]
    status: EmployeeApplicationStatusEnum
    subject: BasicSubjectSchema | None
    subjects: List[BasicSubjectSchema]
    created_at: AwareDatetime


class UpdateEmployeeStatusSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    year_id: uuid.UUID
    employee_ids: List[uuid.UUID]
    status: EmployeeApplicationStatusEnum
