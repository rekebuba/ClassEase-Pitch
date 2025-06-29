from __future__ import annotations
from datetime import date, datetime
from typing import TYPE_CHECKING, Annotated, List, Optional
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

from extension.enums.enum import (
    ExperienceYearEnum,
    GenderEnum,
    HighestDegreeEnum,
    MaritalStatusEnum,
    ScheduleEnum,
    StatusEnum,
)
from extension.functions.helper import to_camel


if TYPE_CHECKING:
    from .user_schema import UserSchema
    from .subject_schema import SubjectSchema
    from .grade_schema import GradeSchema


def parse_and_validate_date(v: str | date) -> date:
    """Parse string and validate date logic"""
    parsed: date | None = None

    if isinstance(v, str):
        try:
            parsed = datetime.strptime(v, "%a, %d %b %Y %H:%M:%S %Z").date()
        except ValueError:
            try:
                parsed = date.fromisoformat(v)
            except ValueError:
                raise ValueError("Date must be in RFC1123 or YYYY-MM-DD format")
    elif isinstance(v, date):
        parsed = v
    else:
        raise ValueError("Invalid date format")

    return parsed


def parse_and_validate_datetime(v: str | datetime) -> datetime:
    """Parse string and validate datetime logic"""
    parsed: datetime | None = None

    if isinstance(v, str):
        try:
            parsed = datetime.strptime(v, "%a, %d %b %Y %H:%M:%S %Z")
        except ValueError:
            try:
                parsed = datetime.fromisoformat(v)
            except ValueError:
                raise ValueError("Datetime must be in RFC1123 or ISO 8601 format")
    elif isinstance(v, datetime):
        parsed = v
    else:
        raise ValueError("Invalid datetime format")

    return parsed


CustomDate = Annotated[date, BeforeValidator(parse_and_validate_date)]
CustomDateTime = Annotated[datetime, BeforeValidator(parse_and_validate_datetime)]


class TeacherSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    first_name: str
    father_name: str
    grand_father_name: str
    date_of_birth: CustomDate
    gender: GenderEnum

    nationality: str
    social_security_number: str

    # Contact Information
    address: str
    city: str
    state: str
    postal_code: str
    country: str
    primary_phone: str
    personal_email: str

    # Emergency Contact
    emergency_contact_name: str
    emergency_contact_relation: str
    emergency_contact_phone: str
    emergency_contact_email: str

    # Educational Background
    highest_degree: HighestDegreeEnum
    university: str
    graduation_year: int
    gpa: float

    # Teaching Experience
    position_applying_for: str
    years_of_experience: ExperienceYearEnum

    preferred_schedule: ScheduleEnum

    # Background & References
    reference1_name: str
    reference1_title: str
    reference1_organization: str
    reference1_phone: str
    reference1_email: str

    # Additional Information (Default values)
    marital_status: Optional[MaritalStatusEnum] = None
    secondary_phone: Optional[str] = None
    additional_degrees: Optional[str] = None
    teaching_license: Optional[bool]
    license_number: Optional[str] = None
    license_state: Optional[str] = None
    license_expiration_date: Optional[CustomDate] = None

    previous_schools: Optional[str] = None

    special_skills: Optional[str] = None
    professional_development: Optional[str] = None

    has_convictions: bool
    conviction_details: Optional[str] = None
    has_disciplinary_actions: bool
    disciplinary_details: Optional[str] = None

    reference2_name: Optional[str] = None
    reference2_title: Optional[str] = None
    reference2_organization: Optional[str] = None
    reference2_phone: Optional[str] = None
    reference2_email: Optional[str] = None
    reference3_name: Optional[str] = None
    reference3_title: Optional[str] = None
    reference3_organization: Optional[str] = None
    reference3_phone: Optional[str] = None
    reference3_email: Optional[str] = None
    resume: Optional[str] = None
    cover_letter: Optional[str] = None
    transcripts: Optional[str] = None
    teaching_certificate: Optional[str] = None
    background_check: Optional[str] = None
    teaching_philosophy: Optional[str] = None
    why_teaching: Optional[str] = None
    additional_comments: Optional[str] = None

    agree_to_terms: bool
    agree_to_background_check: bool

    user_id: Optional[str] = None
    id: Optional[str] = None
    application_date: Optional[CustomDateTime] = Field(default=None, alias="created_at")

    status: StatusEnum = StatusEnum.PENDING


class TeacherRelationshipSchema(BaseModel):
    """This model represents the relationships of a TeacherSchema.
    It is used to define the relationships between the TeacherSchema and other schemas.
    """

    user: Optional[UserSchema]
    subjects_to_teach: Optional[List[SubjectSchema]]
    grade_level: Optional[List[GradeSchema]]
