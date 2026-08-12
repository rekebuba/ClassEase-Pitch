import uuid
from datetime import date
from typing import Any, List, Optional

from pydantic import EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from project.schema.schema import BaseSchema
from project.utils.enum import (
    EmploymentStatusEnum,
    EmploymentTypeEnum,
    RoleEnum,
    SchoolStatusEnum,
)


class NewSchool(BaseSchema):
    name: str = Field(..., description="The name of the school")
    slug: str = Field(..., description="The slug of the school")
    status: SchoolStatusEnum = Field(..., description="The status of the school")
    domain: str | None = Field(None, description="The domain of the school")
    logo_path: str | None = Field(None, description="The path to the school's logo")
    primary_color: str | None = Field(None, description="The primary color of the school")
    settings: dict[str, Any] = Field({"default_language": "en"}, description="The settings of the school")


class SuccessSchoolResponse(BaseSchema):
    message: str = Field(..., description="The success message")
    school_id: uuid.UUID = Field(..., description="The ID of the created school")


class NewSchoolMembership(BaseSchema):
    user_id: uuid.UUID = Field(..., description="The ID of the user")
    role: RoleEnum = Field(..., description="The role of the user in the school")


class SuccessNewSchoolMembership(BaseSchema):
    message: str = Field(..., description="The success message")
    school_id: uuid.UUID = Field(..., description="The ID of the school")
    membership_id: uuid.UUID = Field(..., description="The ID of the membership")
    role_id: uuid.UUID = Field(..., description="The ID of the role assigned to the user")


class ParentProfile(BaseSchema):
    relation: str = Field(min_length=2, max_length=50)
    emergency_contact_phone: Optional[PhoneNumber] = Field(default=None)


class StudentProfile(BaseSchema):
    user_id: uuid.UUID = Field(..., description="The ID of the user")
    is_transfer: bool = Field(default=False, description="Indicates if the student is a transfer student")
    parents: List[ParentProfile] = Field(
        default_factory=list,
        description="List of parent profiles associated with the student",
    )


class EmployeeProfile(BaseSchema):
    user_id: uuid.UUID = Field(..., description="The ID of the user")
    employee_number: str = Field(..., description="The employee number")
    hire_date: date = Field(..., description="The hire date of the employee")
    employment_status: EmploymentStatusEnum = Field(..., description="The employment status")
    employment_type: EmploymentTypeEnum = Field(..., description="The employment type")
    termination_date: Optional[date] = Field(..., description="The termination date of the employee")
    manager_employee_id: Optional[uuid.UUID] = Field(..., description="The ID of the manager employee")
    work_email: Optional[EmailStr] = Field(..., description="The work email of the employee")
    work_phone: Optional[PhoneNumber] = Field(..., description="The work phone number of the employee")
