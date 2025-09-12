import uuid
from datetime import date
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator,
)
from pydantic_extra_types.phone_numbers import PhoneNumber

from utils.enum import BloodTypeEnum, GenderEnum, StudentApplicationStatusEnum
from utils.utils import to_camel


class RegistrationStep(BaseModel):
    message: str


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
    grand_father_name: Optional[str] = Field(default=None)
    date_of_birth: date
    gender: GenderEnum
    nationality: Optional[str] = Field(default=None, min_length=3, max_length=100)


class StudRegStep2(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    registered_for_grade_id: uuid.UUID
    transportation: Optional[str] = Field(default=None)
    is_transfer: bool = Field(default=False)
    previous_school: Optional[str] = Field(default=None, max_length=100)

    @model_validator(mode="after")
    def validate_transfer_details(self) -> "StudRegStep2":
        if self.is_transfer and not self.previous_school:
            raise ValueError("previous_school must be provided if is_transfer is True")
        if not self.is_transfer:
            self.previous_school = None
        return self


class StudRegStep3(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    address: str
    city: str = Field(min_length=3, max_length=50)
    state: str = Field(min_length=3, max_length=50)
    postal_code: str = Field(min_length=3, max_length=20)
    father_phone: PhoneNumber
    mother_phone: PhoneNumber
    parent_email: EmailStr


class StudRegStep4(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    guardian_name: Optional[str] = Field(default=None)
    guardian_phone: Optional[PhoneNumber] = Field(default=None)
    guardian_relation: Optional[str] = Field(default=None)
    emergency_contact_name: Optional[str] = Field(default=None)
    emergency_contact_phone: Optional[PhoneNumber]
    sibling_in_school: bool = Field(default=False)
    sibling_details: Optional[str] = Field(default=None)


class StudRegStep5(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    blood_type: BloodTypeEnum = Field(default=BloodTypeEnum.UNKNOWN)
    student_photo: Optional[str] = Field(default=None)
    has_medical_condition: bool = Field(default=False)
    medical_details: Optional[str] = Field(default=None)
    has_disability: bool = Field(default=False)
    disability_details: Optional[str] = Field(default=None)


class StudentRegistrationForm(
    StudRegStep1,
    StudRegStep2,
    StudRegStep3,
    StudRegStep4,
    StudRegStep5,
):
    status: StudentApplicationStatusEnum = Field(
        default=StudentApplicationStatusEnum.PENDING
    )
