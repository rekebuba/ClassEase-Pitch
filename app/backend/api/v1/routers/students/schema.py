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


class StudentRegisteredYear(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    name: str


class StudentRegisteredGrade(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    grade: GradeEnum
    year: StudentRegisteredYear


class StudentBasicInfo(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID
    full_name: str
    first_name: str
    father_name: str
    grand_father_name: str
    date_of_birth: date
    gender: GenderEnum
    address: str
    city: str
    state: str
    postal_code: str
    father_phone: PhoneNumber
    mother_phone: PhoneNumber
    parent_email: EmailStr
    nationality: Optional[str]
    blood_type: BloodTypeEnum
    student_photo: Optional[str]
    previous_school: Optional[str]
    previous_grades: Optional[str]
    transportation: Optional[str]
    guardian_name: Optional[str]
    guardian_phone: Optional[PhoneNumber]
    guardian_relation: Optional[str]
    emergency_contact_name: Optional[str]
    emergency_contact_phone: Optional[str]
    disability_details: Optional[str]
    sibling_details: Optional[str]
    medical_details: Optional[str]
    sibling_in_school: bool
    has_medical_condition: bool
    has_disability: bool
    is_transfer: bool
    status: StudentApplicationStatusEnum
    created_at: AwareDatetime
    grade: StudentRegisteredGrade


class UpdateStudentStatus(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    status: StudentApplicationStatusEnum
    student_ids: list[uuid.UUID]
