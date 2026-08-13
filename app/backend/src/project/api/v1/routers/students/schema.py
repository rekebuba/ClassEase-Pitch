import uuid
from datetime import date
from typing import Optional

from pydantic import AwareDatetime, EmailStr
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


class EnrollmentApplicationPost(BaseSchema):
    opportunity_id: uuid.UUID
    student_user_id: uuid.UUID
    applicant_note: Optional[str]
    relation: Optional[str]


class EnrollStudentApplication(BaseSchema):
    application_id: uuid.UUID
    student_id: uuid.UUID
    class_section_id: uuid.UUID
    year_id: uuid.UUID
