#!/usr/bin/python3
"""Module for Teacher class"""

from datetime import date
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    Enum,
    Float,
    Integer,
    String,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel


if TYPE_CHECKING:
    from models.user import User  # Avoid circular import
    from models.subject import Subject
    from models.grade import Grade


class Teacher(BaseModel):
    """
    This model represents a teacher in the ClassEase system. It inherits from BaseModel and Base.
    """

    __tablename__ = "teachers"

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    father_name: Mapped[str] = mapped_column(String(50), nullable=False)
    grand_father_name: Mapped[str] = mapped_column(String(50), nullable=False)
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    gender: Mapped[BaseModel.GenderEnum] = mapped_column(
        Enum(
            BaseModel.GenderEnum,
            name="gender_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )
    nationality: Mapped[str] = mapped_column(String(50), nullable=False)
    social_security_number: Mapped[str] = mapped_column(String(50), nullable=False)

    # Contact Information
    address: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(50), nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    primary_phone: Mapped[str] = mapped_column(String(50), nullable=False)
    personal_email: Mapped[str] = mapped_column(String(50), nullable=False)

    # Emergency Contact
    emergency_contact_name: Mapped[str] = mapped_column(String(50), nullable=False)
    emergency_contact_relation: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    emergency_contact_phone: Mapped[str] = mapped_column(String(50), nullable=False)
    emergency_contact_email: Mapped[str] = mapped_column(String(50), nullable=False)

    # Educational Background
    highest_degree: Mapped[BaseModel.HighestDegreeEnum] = mapped_column(
        Enum(
            BaseModel.HighestDegreeEnum,
            name="highest_degree_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )
    university: Mapped[str] = mapped_column(String(50), nullable=False)
    graduation_year: Mapped[int] = mapped_column(Integer, nullable=False)
    gpa: Mapped[float] = mapped_column(Float, nullable=False)

    # Teaching Experience
    position_applying_for: Mapped[str] = mapped_column(String(50), nullable=False)
    years_of_experience: Mapped[BaseModel.ExperienceYearEnum] = mapped_column(
        Enum(
            BaseModel.ExperienceYearEnum,
            name="experience_year_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )

    preferred_schedule: Mapped[BaseModel.ScheduleEnum] = mapped_column(
        Enum(
            BaseModel.ScheduleEnum,
            name="schedule_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )

    # Background & References
    reference1_name: Mapped[str] = mapped_column(String(50), nullable=False)
    reference1_title: Mapped[str] = mapped_column(String(50), nullable=False)
    reference1_organization: Mapped[str] = mapped_column(String(50), nullable=False)
    reference1_phone: Mapped[str] = mapped_column(String(50), nullable=False)
    reference1_email: Mapped[str] = mapped_column(String(50), nullable=False)

    # Additional Information (Default values)
    marital_status: Mapped[Optional[BaseModel.MaritalStatusEnum]] = mapped_column(
        Enum(
            BaseModel.MaritalStatusEnum,
            name="marital_status_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=True,
        default=None,
    )

    secondary_phone: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    additional_degrees: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, default=None
    )
    teaching_license: Optional[bool] = False
    license_number: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    license_state: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    license_expiration_date: Mapped[Optional[date]] = mapped_column(
        Date, nullable=True, default=None
    )

    certifications: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, default=None
    )
    specializations: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, default=None
    )
    previous_schools: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, default=None
    )

    special_skills: Mapped[Optional[str]] = mapped_column(Text, default=None)
    professional_development: Mapped[Optional[str]] = mapped_column(Text, default=None)

    has_convictions: Mapped[bool] = mapped_column(Boolean, default=False)
    conviction_details: Mapped[Optional[str]] = mapped_column(Text, default=None)
    has_disciplinary_actions: Mapped[bool] = mapped_column(Boolean, default=False)
    disciplinary_details: Mapped[Optional[str]] = mapped_column(Text, default=None)

    reference2_name: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    reference2_title: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    reference2_organization: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    reference2_phone: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    reference2_email: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    reference3_name: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    reference3_title: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    reference3_organization: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    reference3_phone: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    reference3_email: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    resume: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    cover_letter: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    transcripts: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    teaching_certificate: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    background_check: Mapped[Optional[str]] = mapped_column(Text, default=None)
    teaching_philosophy: Mapped[Optional[str]] = mapped_column(Text, default=None)
    why_teaching: Mapped[Optional[str]] = mapped_column(Text, default=None)
    additional_comments: Mapped[Optional[str]] = mapped_column(Text, default=None)

    agree_to_terms: Mapped[bool] = mapped_column(Boolean, default=False)
    agree_to_background_check: Mapped[bool] = mapped_column(Boolean, default=False)

    user_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("users.id"), unique=True, nullable=True, default=None
    )

    status: Mapped[BaseModel.StatusEnum] = mapped_column(
        Enum(
            BaseModel.StatusEnum,
            name="status_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=BaseModel.StatusEnum.PENDING,
    )

    # Relationship with Default
    user: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="teachers",
        default=None,
    )
    # Relationship with Out Default
    subjects_to_teach: Mapped[List["Subject"]] = relationship(
        "Subject",
        back_populates="teachers",
        secondary="teacher_subject_links",
        default_factory=list,
    )
    grade_level: Mapped[List["Grade"]] = relationship(
        "Grade",
        back_populates="teachers",
        secondary="teacher_grade_links",
        default_factory=list,
    )

    __table_args__ = (
        CheckConstraint("gpa >= 0.0 AND gpa <= 4.0", name="check_teacher_gpa_range"),
        CheckConstraint(
            "(has_convictions = 0 OR conviction_details IS NOT NULL)",
            name="check_conviction_details",
        ),
        CheckConstraint(
            "(has_disciplinary_actions = 0 OR disciplinary_details IS NOT NULL)",
            name="check_disciplinary_details",
        ),
    )
