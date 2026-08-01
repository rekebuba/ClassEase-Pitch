import uuid
from typing import List, Optional

from project.schema.schema import BaseSchema
from project.utils.enum import EmploymentStatusEnum, HighestEducationEnum


class TeacherBasicInfo(BaseSchema):
    teacher_profile_id: uuid.UUID
    employee_id: uuid.UUID
    user_id: Optional[uuid.UUID]
    employee_number: str
    employment_status: EmploymentStatusEnum
    full_name: Optional[str]
    work_email: Optional[str]
    specialization: Optional[str]
    subject_ids: List[uuid.UUID]


class TeachersQuery(BaseSchema):
    q: Optional[str] = None
    academic_year_id: Optional[uuid.UUID] = None


class CreateTeacherProfile(BaseSchema):
    employee_id: uuid.UUID
    specialization: Optional[str] = None
    teacher_license_number: Optional[str] = None
    certifications: Optional[str] = None
    highest_education: Optional[HighestEducationEnum] = None
    years_of_experience: Optional[int] = None


class AssignTeacher(BaseSchema):
    teacher_profile_id: uuid.UUID
    subject_id: uuid.UUID
    class_section_id: uuid.UUID
    academic_year_id: uuid.UUID
    weekly_periods: int = 0
    room_id: Optional[uuid.UUID] = None


class TeacherProfileUpdate(BaseSchema):
    specialization: Optional[str] = None
    teacher_license_number: Optional[str] = None
    certifications: Optional[str] = None
    highest_education: Optional[HighestEducationEnum] = None
    years_of_experience: Optional[int] = None
