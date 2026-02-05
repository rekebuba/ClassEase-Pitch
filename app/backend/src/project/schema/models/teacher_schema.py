from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from project.schema.models.academic_term_schema import AcademicTermSchema
from project.utils.enum import (
    EmployeeApplicationStatusEnum,
    ExperienceYearEnum,
    GenderEnum,
    HighestEducationEnum,
    MaritalStatusEnum,
    ScheduleEnum,
)
from project.utils.utils import to_camel

if TYPE_CHECKING:
    from project.schema.models.grade_schema import GradeSchema
    from project.schema.models.section_schema import SectionSchema
    from project.schema.models.subject_schema import SubjectSchema
    from project.schema.models.user_schema import UserSchema
    from project.schema.models.year_schema import YearSchema


class TeacherSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID | None = None
    first_name: str
    father_name: str
    grand_father_name: str
    date_of_birth: date
    gender: GenderEnum
    nationality: str
    social_security_number: str
    address: str
    city: str
    state: str
    postal_code: str
    country: str
    primary_phone: str
    personal_email: str
    emergency_contact_name: str
    emergency_contact_relation: str
    emergency_contact_phone: str
    emergency_contact_email: str
    highest_degree: HighestEducationEnum
    university: str
    graduation_year: int
    gpa: float
    position_applying_for: str
    years_of_experience: ExperienceYearEnum
    preferred_schedule: ScheduleEnum
    reference1_name: str
    reference1_title: str
    reference1_organization: str
    reference1_phone: str
    reference1_email: str
    marital_status: Optional[MaritalStatusEnum] = None
    secondary_phone: Optional[str] = None
    additional_degrees: Optional[str] = None
    teaching_license: Optional[bool] = False
    license_number: Optional[str] = None
    license_state: Optional[str] = None
    license_expiration_date: Optional[date] = None
    certifications: Optional[str] = None
    specializations: Optional[str] = None
    previous_schools: Optional[str] = None
    special_skills: Optional[str] = None
    professional_development: Optional[str] = None
    has_convictions: bool = False
    conviction_details: Optional[str] = None
    has_disciplinary_actions: bool = False
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
    agree_to_terms: bool = False
    agree_to_background_check: bool = False
    user_id: Optional[uuid.UUID] = None
    status: EmployeeApplicationStatusEnum = EmployeeApplicationStatusEnum.PENDING

    @classmethod
    def default_fields(cls) -> set[str]:
        """
        Returns a list of default fields to be used
        when no specific fields are requested.
        This can be overridden in subclasses if needed.
        """
        return {"id", "first_name", "father_name", "date_of_birth"}


class TeacherRelatedSchema(BaseModel):
    """This model represents the relationships of a TeacherSchema.
    It is used to define the relationships between the TeacherSchema and other schemas.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    user: Optional[UserSchema] = None
    sections: Optional[List[SectionSchema]] = []
    years: Optional[List[YearSchema]] = Field(
        default=None,
        description="List of years the teacher is associated with.",
    )
    academic_terms: Optional[List[AcademicTermSchema]] = Field(
        default=None,
        description="List of academic terms the teacher is associated with.",
    )
    grades: Optional[List[GradeSchema]] = Field(
        default=None,
        description="List of grades the teacher is associated with.",
    )
    subjects: Optional[List[SubjectSchema]] = Field(
        default=None,
        description="List of subjects the teacher is associated with.",
    )


class TeacherWithRelatedSchema(TeacherSchema, TeacherRelatedSchema):
    """This model extends TeacherSchema to include relationships."""

    pass
