from datetime import date
from typing import TYPE_CHECKING, List, Optional
from pydantic import BaseModel, ConfigDict
from models.base_model import CustomTypes


if TYPE_CHECKING:
    from .user_schema import UserSchema
    from .subject_schema import SubjectSchema
    from .grade_schema import GradeSchema


class TeacherSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    father_name: str
    grand_father_name: str
    date_of_birth: date
    gender: CustomTypes.GenderEnum

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
    emergency_contact_relationship: str
    emergency_contact_phone: str
    emergency_contact_email: str

    # Educational Background
    highest_degree: str
    major_subject: str
    university: str
    graduation_year: int
    gpa: float

    # Teaching Experience
    position_applying_for: str
    years_of_experience: CustomTypes.ExperienceYearEnum

    preferred_schedule: CustomTypes.ScheduleEnum

    # Background & References
    reference1_name: str
    reference1_title: str
    reference1_organization: str
    reference1_phone: str
    reference1_email: str

    # Additional Information (Default values)
    preferred_name: Optional[str]
    secondary_phone: Optional[str]
    work_email: Optional[str]
    minor_subject: Optional[str]
    additional_degrees: Optional[str]
    teaching_license: Optional[bool]
    license_number: Optional[str]
    license_state: Optional[str]
    license_expiration_date: Optional[date]

    certifications: Optional[str]
    specializations: Optional[str]
    previous_schools: Optional[str]

    languages_spoken: Optional[str]
    technology_skills: Optional[str]
    special_skills: Optional[str]
    professional_development: Optional[str]

    has_convictions: bool
    conviction_details: Optional[str]
    has_disciplinary_actions: bool
    disciplinary_details: Optional[str]

    reference2_name: Optional[str]
    reference2_title: Optional[str]
    reference2_organization: Optional[str]
    reference2_phone: Optional[str]
    reference2_email: Optional[str]
    reference3_name: Optional[str]
    reference3_title: Optional[str]
    reference3_organization: Optional[str]
    reference3_phone: Optional[str]
    reference3_email: Optional[str]
    resume: Optional[str]
    cover_letter: Optional[str]
    transcripts: Optional[str]
    teaching_certificate: Optional[str]
    background_check: Optional[str]
    teaching_philosophy: Optional[str]
    why_teaching: Optional[str]
    additional_comments: Optional[str]

    agree_to_terms: bool
    agree_to_background_check: bool

    user_id: str

    # Relationship
    user: Optional[UserSchema]
    subjects_to_teach: Optional[List[SubjectSchema]]
    grade_level: Optional[List[GradeSchema]]
