import uuid
from datetime import date
from typing import Optional

from pydantic import (
    EmailStr,
    Field,
    PastDate,
    SecretStr,
    model_validator,
)
from pydantic_extra_types.phone_numbers import PhoneNumber

from project.schema.schema import BaseSchema
from project.utils.enum import (
    BloodTypeEnum,
    EmploymentStatusEnum,
    EmploymentTypeEnum,
    GenderEnum,
    HighestEducationEnum,
    StudentApplicationStatusEnum,
)


class RegistrationStep(BaseSchema):
    message: str


class RegistrationResponse(BaseSchema):
    """
    Schema for successful registration response.
    """

    id: uuid.UUID
    message: str


class UserRegistration(BaseSchema):
    first_name: str
    father_name: str
    grand_father_name: Optional[str]
    date_of_birth: PastDate
    gender: GenderEnum
    email: EmailStr
    phone: Optional[PhoneNumber] = None
    username: Optional[str] = None
    password: Optional[SecretStr] = None


class AdminRegistration(UserRegistration):
    pass


class ParentRegistrationForm(UserRegistration):
    relation: str = Field(min_length=2, max_length=50)
    emergency_contact_phone: Optional[PhoneNumber] = Field(default=None)


class ParentRegistrationMe(BaseSchema):
    relation: str = Field(min_length=2, max_length=50)
    emergency_contact_phone: Optional[PhoneNumber] = Field(default=None)


class StudRegStep1(BaseSchema):
    first_name: str = Field(min_length=2, max_length=50)
    father_name: str = Field(min_length=2, max_length=50)
    grand_father_name: Optional[str] = Field(default=None)
    date_of_birth: PastDate
    gender: GenderEnum
    nationality: Optional[str] = Field(default=None, min_length=2, max_length=100)
    student_photo: Optional[str] = Field(default=None)


class StudRegStep2(BaseSchema):
    registered_for_grade_id: uuid.UUID
    transportation: Optional[str] = Field(default=None)
    is_transfer: bool = Field(default=False)
    previous_school: Optional[str] = Field(default=None, max_length=100)

    @model_validator(mode="after")
    def validate_transfer_details(self) -> "StudRegStep2":
        if self.is_transfer and not self.previous_school:
            raise ValueError("previousSchool Must be provided if student is Transferred")
        if not self.is_transfer:
            self.previous_school = None
        return self


class StudRegStep3(BaseSchema):
    city: str = Field(min_length=2, max_length=50)
    state: str = Field(min_length=2, max_length=50)
    postal_code: str = Field(min_length=2, max_length=20)


class StudRegStep4(BaseSchema):
    emergency_contact_name: Optional[str] = Field(default=None)
    emergency_contact_phone: Optional[PhoneNumber]


class StudRegStep5(BaseSchema):
    blood_type: BloodTypeEnum = Field(default=BloodTypeEnum.UNKNOWN)
    has_medical_condition: bool = Field(default=False)
    medical_details: Optional[str] = Field(default=None)
    has_disability: bool = Field(default=False)
    disability_details: Optional[str] = Field(default=None)

    @model_validator(mode="after")
    def validate_medical_details(self) -> "StudRegStep5":
        if self.has_medical_condition and not self.medical_details:
            raise ValueError("medicalDetails Must be provided if has Medical Conditions")
        if not self.has_medical_condition:
            self.medical_details = None

        if self.has_disability and not self.disability_details:
            raise ValueError("disabilityDetails Must be provided if has Disability")
        if not self.has_disability:
            self.disability_details = None

        return self


class StudentRegistrationForm(
    UserRegistration,
    StudRegStep1,
    StudRegStep2,
    StudRegStep3,
    StudRegStep4,
    StudRegStep5,
):
    parent_id: uuid.UUID
    status: StudentApplicationStatusEnum = Field(default=StudentApplicationStatusEnum.PENDING)


class StudentRegistrationMe(
    StudRegStep2,
    StudRegStep3,
    StudRegStep4,
    StudRegStep5,
):
    nationality: Optional[str] = Field(default=None, min_length=2, max_length=100)
    student_photo: Optional[str] = Field(default=None)
    parent_id: Optional[uuid.UUID] = None
    status: StudentApplicationStatusEnum = Field(default=StudentApplicationStatusEnum.PENDING)


class EmployeeRegStep1(BaseSchema):
    employee_number: str
    hire_date: date
    employment_type: EmploymentTypeEnum = EmploymentTypeEnum.FULL_TIME


class EmployeeRegStep2(BaseSchema):
    email: EmailStr
    phone: PhoneNumber
    department_id: Optional[uuid.UUID] = Field(default=None)
    primary_position_id: Optional[uuid.UUID] = Field(default=None)
    manager_employee_id: Optional[uuid.UUID] = Field(default=None)


class EmployeeRegStep3(BaseSchema):
    status: EmploymentStatusEnum = EmploymentStatusEnum.ACTIVE
    termination_date: Optional[date] = Field(default=None)
    highest_education: Optional[HighestEducationEnum] = Field(default=None)


class EmployeeRegStep4(BaseSchema):
    agree_to_terms: bool = Field(validate_default=True)
    agree_to_background_check: bool = Field(validate_default=True)


class EmployeeRegistrationForm(
    UserRegistration,
    EmployeeRegStep1,
    EmployeeRegStep2,
    EmployeeRegStep3,
    EmployeeRegStep4,
):
    pass
