import uuid
from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from utils.enum import BloodTypeEnum, GenderEnum, StudentApplicationStatusEnum
from utils.utils import to_camel


class RegistrationResponse(BaseModel):
    """
    Schema for successful registration response.
    """

    id: uuid.UUID
    message: str


class StudRegStep1(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    first_name: str = Field(min_length=3, max_length=50)
    father_name: str = Field(min_length=3, max_length=50)
    date_of_birth: date = Field(min_length=3, max_length=50)
    gender: GenderEnum = Field(min_length=3, max_length=50)
    nationality: Optional[str] = Field(default=None)

class StudRegStep2(BaseModel):

    registered_for_grade_id: uuid.UUID
    transportation: Optional[str] = Field(default=None)


# class StudRegStep3(BaseModel):
# class StudRegStep4(BaseModel):
# class StudRegStep5(BaseModel):



class StudentRegistrationForm(StudRegStep1):

    address: str
    city: str
    state: str
    postal_code: str
    father_phone: str
    mother_phone: str
    parent_email: str
    grand_father_name: Optional[str] = Field(default=None)
    blood_type: BloodTypeEnum = Field(default=BloodTypeEnum.UNKNOWN)
    student_photo: Optional[str] = Field(default=None)
    previous_school: Optional[str] = Field(default=None)
    previous_grades: Optional[str] = Field(default=None)
    guardian_name: Optional[str] = Field(default=None)
    guardian_phone: Optional[str] = Field(default=None)
    guardian_relation: Optional[str] = Field(default=None)
    emergency_contact_name: Optional[str] = Field(default=None)
    emergency_contact_phone: Optional[str] = Field(default=None)
    disability_details: Optional[str] = Field(default=None)
    sibling_details: Optional[str] = Field(default=None)
    medical_details: Optional[str] = Field(default=None)
    sibling_in_school: bool = Field(default=False)
    has_medical_condition: bool = Field(default=False)
    has_disability: bool = Field(default=False)
    is_transfer: bool = Field(default=False)
    status: StudentApplicationStatusEnum = Field(
        default=StudentApplicationStatusEnum.PENDING
    )
