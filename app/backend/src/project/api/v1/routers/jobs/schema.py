import uuid
from datetime import date
from typing import Optional

from pydantic import EmailStr, Field

from project.schema.schema import BaseSchema
from project.utils.enum import (
    ContractTypeEnum,
    EmploymentStatusEnum,
    EmploymentTypeEnum,
    HighestEducationEnum,
)


class JobPost(BaseSchema):
    position_id: uuid.UUID = Field(..., description="The ID of the position")
    description: str = Field(..., description="The description of the job")
    employment_type: EmploymentTypeEnum = Field(..., description="The employment type of the job")
    application_deadline: Optional[date] = Field(None, description="The application deadline for the job")
    openings_count: int = Field(..., description="The number of openings for the job")


class JobApplicationPost(BaseSchema):
    job_id: uuid.UUID = Field(..., description="The ID of the job posting")
    cover_note: Optional[str] = Field(None, description="The cover note for the application")


class TeacherProfileJob(BaseSchema):
    specialization: str | None = Field(None, description="The specialization of the teacher")
    teacher_license_number: str | None = Field(None, description="The license number of the teacher")
    certifications: str | None = Field(None, description="The certification of the teacher")
    highest_education: HighestEducationEnum | None = Field(
        None, description="The highest education level of the teacher"
    )
    years_of_experience: int | None = Field(None, description="The years of experience of the teacher")


class HireJobApplication(BaseSchema):
    application_id: uuid.UUID = Field(..., description="The ID of the employment application")
    employee_number: str = Field(..., description="The employee number assigned to the new employee")
    hire_date: date = Field(..., description="The date the employee was hired")
    employment_status: EmploymentStatusEnum = Field(..., description="The employment status of the employee")
    employment_type: EmploymentTypeEnum = Field(..., description="The type of employment")
    termination_date: Optional[date] = Field(None, description="The date the employee was terminated")
    manager_employee_id: Optional[uuid.UUID] = Field(None, description="The ID of the employee's manager")
    work_email: EmailStr = Field(..., description="The work email of the employee")
    work_phone: str = Field(..., description="The work phone number of the employee")

    start_date: date = Field(..., description="The start date of the employee's position")
    end_date: date | None = Field(None, description="The end date of the employee's position")

    contract_type: ContractTypeEnum = Field(..., description="The type of employment contract for the employee")
    contract_start_date: date = Field(..., description="The start date of the employment contract")
    contract_end_date: date | None = Field(None, description="The end date of the employment contract")
    hours_per_week: int = Field(..., description="The number of hours per week for the employment contract")

    teacher_profile: TeacherProfileJob | None = Field(
        None, description="The teacher profile information for the employee, if applicable"
    )
