import uuid
from datetime import date
from typing import List, Optional

from pydantic import AwareDatetime, BaseModel, ConfigDict, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from utils.enum import (
    EmployeeApplicationStatusEnum,
    ExperienceYearEnum,
    GenderEnum,
    HighestEducationEnum,
    MaritalStatusEnum,
)
from utils.utils import to_camel


class TeacherAppliedSubject(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    name: str


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
    primary_phone: PhoneNumber
    personal_email: EmailStr
    emergency_contact_name: str
    emergency_contact_relation: str
    emergency_contact_phone: PhoneNumber
    highest_education: HighestEducationEnum
    university: str
    graduation_year: int
    gpa: float
    position: str
    years_of_experience: ExperienceYearEnum
    reference1_name: str
    reference1_organization: str
    reference1_phone: PhoneNumber
    reference1_email: Optional[EmailStr]
    marital_status: Optional[MaritalStatusEnum]
    secondary_phone: Optional[str]
    resume: Optional[str]
    status: EmployeeApplicationStatusEnum
    created_at: AwareDatetime
    subjects: List[TeacherAppliedSubject]


class UpdateEmployeeStatusSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    year_id: uuid.UUID
    employee_ids: List[uuid.UUID]
    status: EmployeeApplicationStatusEnum
