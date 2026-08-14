import uuid
from datetime import date
from typing import Optional

from pydantic import AwareDatetime, EmailStr, model_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from project.schema.models import GradeSchema, YearSchema
from project.schema.schema import BaseSchema
from project.utils.enum import (
    BloodTypeEnum,
    GenderEnum,
    GradeEnum,
    StudentApplicationStatusEnum,
)


class StudentRegisteredYear(BaseSchema):
    id: uuid.UUID
    name: str


class StudentRegisteredGrade(BaseSchema):
    id: uuid.UUID
    grade: GradeEnum
    year: StudentRegisteredYear


class StudentBasicInfo(BaseSchema):
    first_name: str
    father_name: str
    grand_father_name: str
    date_of_birth: date
    gender: GenderEnum
    email: Optional[EmailStr]
    phone: Optional[PhoneNumber]


class UpdateStudentStatus(BaseSchema):
    status: StudentApplicationStatusEnum
    student_ids: list[uuid.UUID]


class EnrollStudent(BaseSchema):
    student_id: uuid.UUID
    class_section_id: uuid.UUID
    year_id: uuid.UUID


class EnrollmentOpportunityPost(BaseSchema):
    academic_year_id: uuid.UUID
    grade_id: uuid.UUID
    application_deadline: Optional[AwareDatetime]
    capacity: int
    allow_applications: bool


class EnrollmentOpportunitySchema(BaseSchema):
    id: uuid.UUID
    academic_year_id: YearSchema
    grade_id: GradeSchema
    application_deadline: Optional[AwareDatetime]
    capacity: int
    allow_applications: bool
    status: StudentApplicationStatusEnum
    created_at: AwareDatetime
    updated_at: AwareDatetime


class HealthRecord(BaseSchema):
    blood_type: BloodTypeEnum
    has_disability: bool
    disability_details: Optional[str]
    has_medical_condition: bool
    medical_details: Optional[str]

    @model_validator(mode="after")
    def validate_medical_details(self) -> "HealthRecord":
        if self.has_medical_condition and not self.medical_details:
            raise ValueError("medicalDetails Must be provided if has Medical Conditions")
        if not self.has_medical_condition:
            self.medical_details = None

        if self.has_disability and not self.disability_details:
            raise ValueError("disabilityDetails Must be provided if has Disability")
        if not self.has_disability:
            self.disability_details = None

        return self


class AcademicBackground(BaseSchema):
    previous_school: Optional[str]
    is_transfer: bool

    @model_validator(mode="after")
    def validate_transfer_details(self) -> "AcademicBackground":
        if self.is_transfer and not self.previous_school:
            raise ValueError("previousSchool Must be provided if student is Transferred")
        if not self.is_transfer:
            self.previous_school = None
        return self


class Address(BaseSchema):
    city: str
    state: str
    postal_code: str
    nationality: str
    transportation: str


class EnrollmentApplicationPost(BaseSchema):
    opportunity_id: uuid.UUID
    student_user_id: uuid.UUID | None
    applicant_note: Optional[str]
    relation: Optional[str]

    user: StudentBasicInfo | None
    health_record: HealthRecord
    academic_background: AcademicBackground
    address: Address

    @model_validator(mode="after")
    def validate_student_user_id(self) -> "EnrollmentApplicationPost":
        if self.student_user_id is None and self.user is None:
            raise ValueError("Either student_user_id or user must be provided")
        return self


class EnrollStudentApplication(BaseSchema):
    application_id: uuid.UUID
    student_id: uuid.UUID
    class_section_id: uuid.UUID
    year_id: uuid.UUID
