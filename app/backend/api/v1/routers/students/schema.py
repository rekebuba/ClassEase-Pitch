import uuid
from datetime import date
from typing import Optional

from pydantic import AwareDatetime, BaseModel, ConfigDict, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from utils.enum import (
    BloodTypeEnum,
    GenderEnum,
    GradeEnum,
    StudentApplicationStatusEnum,
)
from utils.utils import to_camel


class StudentCurrentGrade(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    grade: GradeEnum


class StudentBasicInfo(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    first_name: str
    father_name: str
    grand_father_name: Optional[str]
    date_of_birth: date
    gender: GenderEnum
    address: str
    city: str
    state: str
    postal_code: str
    father_phone: PhoneNumber
    mother_phone: PhoneNumber
    parent_email: EmailStr
    blood_type: BloodTypeEnum = BloodTypeEnum.UNKNOWN
    previous_school: Optional[str]
    guardian_name: Optional[str]
    guardian_phone: Optional[PhoneNumber]
    guardian_relation: Optional[str]
    sibling_in_school: bool
    has_medical_condition: bool
    has_disability: bool
    is_transfer: bool
    status: StudentApplicationStatusEnum
    grade: StudentCurrentGrade
    created_at: AwareDatetime
