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

from utils.enum import (
    BloodTypeEnum,
    EmployeeApplicationStatusEnum,
    EmployeePositionEnum,
    ExperienceYearEnum,
    GenderEnum,
    HighestEducationEnum,
    MaritalStatusEnum,
    StudentApplicationStatusEnum,
)
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
    student_photo: Optional[str] = Field(default=None)


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
            raise ValueError(
                "previousSchool Must be provided if student is Transferred"
            )
        if not self.is_transfer:
            self.previous_school = Field(default=None)
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
    has_medical_condition: bool = Field(default=False)
    medical_details: Optional[str] = Field(default=None)
    has_disability: bool = Field(default=False)
    disability_details: Optional[str] = Field(default=None)

    @model_validator(mode="after")
    def validate_medical_details(self) -> "StudRegStep5":
        if self.has_medical_condition and not self.medical_details:
            raise ValueError(
                "medicalDetails Must be provided if has Medical Conditions"
            )
        if not self.has_medical_condition:
            self.medical_details = Field(default=None)

        if self.has_disability and not self.disability_details:
            raise ValueError("disabilityDetails Must be provided if has Disability")
        if not self.has_disability:
            self.disability_details = Field(default=None)

        return self


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


class EmployeeRegStep1(BaseModel):
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
    marital_status: Optional[MaritalStatusEnum] = Field(default=None)
    social_security_number: str


class EmployeeRegStep2(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    address: str
    city: str = Field(min_length=3, max_length=50)
    state: str = Field(min_length=3, max_length=50)
    country: str
    primary_phone: PhoneNumber
    secondary_phone: Optional[PhoneNumber] = Field(default=None)
    personal_email: EmailStr
    emergency_contact_name: str = Field(min_length=3, max_length=50)
    emergency_contact_relation: str = Field(min_length=3, max_length=50)
    emergency_contact_phone: PhoneNumber


class EmployeeRegStep3(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    highest_education: HighestEducationEnum
    subject_id: Optional[uuid.UUID] = Field(default=None)
    university: str
    graduation_year: int
    gpa: float
    position: EmployeePositionEnum
    years_of_experience: ExperienceYearEnum

    @model_validator(mode="after")
    def validate_education_details(self) -> "EmployeeRegStep3":
        if self.position == EmployeePositionEnum.TEACHING_STAFF:
            if not self.subject_id:
                raise ValueError(
                    "subjectId must be provided for teachers applying for the position"
                )
        else:
            self.subject_id = None
        return self


class EmployeeRegStep4(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    reference1_name: str
    reference1_organization: str
    reference1_phone: str
    reference1_email: Optional[EmailStr] = Field(default=None)


class EmployeeRegStep5(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    resume: Optional[str] = Field(default=None)
    background_check: Optional[str] = Field(default=None)
    agree_to_terms: bool = Field(validate_default=True)
    agree_to_background_check: bool = Field(validate_default=True)


class EmployeeRegistrationForm(
    EmployeeRegStep1,
    EmployeeRegStep2,
    EmployeeRegStep3,
    EmployeeRegStep4,
    EmployeeRegStep5,
):
    status: EmployeeApplicationStatusEnum = EmployeeApplicationStatusEnum.PENDING
