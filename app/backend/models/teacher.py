#!/usr/bin/python3
"""Module for Teacher class"""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base.base_model import BaseModel
from models.base.column_type import UUIDType
from models.teacher_record import TeacherRecord
from utils.enum import (
    ExperienceYearEnum,
    GenderEnum,
    HighestDegreeEnum,
    MaritalStatusEnum,
    TeacherApplicationStatus,
)

if TYPE_CHECKING:
    from models.academic_term import AcademicTerm
    from models.grade import Grade
    from models.section import Section
    from models.subject import Subject
    from models.teacher_term_record import TeacherTermRecord
    from models.user import User
    from models.year import Year


class Teacher(BaseModel):
    """
    This model represents a teacher in the ClassEase system.
    It inherits from BaseModel and Base.
    """

    __tablename__ = "teachers"

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    father_name: Mapped[str] = mapped_column(String(50), nullable=False)
    grand_father_name: Mapped[str] = mapped_column(String(50), nullable=False)
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    gender: Mapped[GenderEnum] = mapped_column(
        Enum(
            GenderEnum,
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
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    primary_phone: Mapped[str] = mapped_column(String(50), nullable=False)
    personal_email: Mapped[str] = mapped_column(String(50), nullable=False)

    # Emergency Contact
    emergency_contact_name: Mapped[str] = mapped_column(String(50), nullable=False)
    emergency_contact_relation: Mapped[str] = mapped_column(String(50), nullable=False)
    emergency_contact_phone: Mapped[str] = mapped_column(String(50), nullable=False)

    # Educational Background
    highest_degree: Mapped[HighestDegreeEnum] = mapped_column(
        Enum(
            HighestDegreeEnum,
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
    years_of_experience: Mapped[ExperienceYearEnum] = mapped_column(
        Enum(
            ExperienceYearEnum,
            name="experience_year_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )
    teaching_license: bool

    # Background & References
    reference1_name: Mapped[str] = mapped_column(String(50), nullable=False)
    reference1_organization: Mapped[str] = mapped_column(String(50), nullable=False)
    reference1_phone: Mapped[str] = mapped_column(String(50), nullable=False)

    # Additional Information (Default values)
    reference1_email: Mapped[Optional[str]] = mapped_column(String(50), default=None)
    marital_status: Mapped[Optional[MaritalStatusEnum]] = mapped_column(
        Enum(
            MaritalStatusEnum,
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

    certifications: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, default=None
    )

    resume: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    background_check: Mapped[Optional[str]] = mapped_column(Text, default=None)

    agree_to_terms: Mapped[bool] = mapped_column(Boolean, default=False)
    agree_to_background_check: Mapped[bool] = mapped_column(Boolean, default=False)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=True,
        default=None,
    )

    status: Mapped[TeacherApplicationStatus] = mapped_column(
        Enum(
            TeacherApplicationStatus,
            name="status_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=TeacherApplicationStatus.PENDING,
    )

    # Relationship with Default
    user: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="teacher",
        init=False,
        repr=False,
        passive_deletes=True,
    )

    # Many-to-Many Relationship
    years: Mapped[List["Year"]] = relationship(
        "Year",
        back_populates="teachers",
        secondary="teacher_year_links",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    academic_terms: Mapped[List["AcademicTerm"]] = relationship(
        "AcademicTerm",
        back_populates="teachers",
        secondary="teacher_academic_term_links",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    subjects: Mapped[List["Subject"]] = relationship(
        "Subject",
        back_populates="teachers",
        secondary="teacher_subject_links",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    grades: Mapped[List["Grade"]] = relationship(
        "Grade",
        back_populates="teachers",
        secondary="teacher_grade_links",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    sections: Mapped[List["Section"]] = relationship(
        "Section",
        back_populates="teachers",
        secondary="teacher_section_links",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    # One-To-Many Relationships
    teacher_records: Mapped[List["TeacherRecord"]] = relationship(
        "TeacherRecord",
        back_populates="teacher",
        default_factory=list,
        repr=False,
        passive_deletes=True,
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
