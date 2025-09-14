#!/usr/bin/python3
"""Module for Student class"""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    Boolean,
    Date,
    Enum,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base.base_model import BaseModel
from models.base.column_type import UUIDType
from utils.enum import BloodTypeEnum, GenderEnum, StudentApplicationStatusEnum

if TYPE_CHECKING:
    from models.academic_term import AcademicTerm
    from models.assessment import Assessment
    from models.grade import Grade
    from models.mark_list import MarkList
    from models.section import Section
    from models.stream import Stream
    from models.student_term_record import StudentTermRecord
    from models.subject import Subject
    from models.subject_yearly_average import SubjectYearlyAverage
    from models.user import User
    from models.year import Year


class Student(BaseModel):
    """
    Represents a student entity in the database.
    """

    __tablename__ = "students"

    registered_for_grade_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("grades.id", ondelete="SET NULL"),
        nullable=True,
    )
    # Personal Information
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    father_name: Mapped[str] = mapped_column(String(50), nullable=False)
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

    # Contact Information
    address: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=False)
    father_phone: Mapped[str] = mapped_column(String(25), nullable=False)
    mother_phone: Mapped[str] = mapped_column(String(25), nullable=False)
    parent_email: Mapped[str] = mapped_column(String(120), nullable=False)

    grand_father_name: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    nationality: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, default=None
    )
    blood_type: Mapped[BloodTypeEnum] = mapped_column(
        Enum(
            BloodTypeEnum,
            name="blood_type_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=True,
        default=BloodTypeEnum.UNKNOWN,
    )
    student_photo: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, default=None
    )
    previous_school: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, default=None
    )
    previous_grades: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, default=None
    )
    transportation: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    guardian_name: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    guardian_phone: Mapped[Optional[str]] = mapped_column(
        String(25), nullable=True, default=None
    )
    guardian_relation: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    emergency_contact_name: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    emergency_contact_phone: Mapped[Optional[str]] = mapped_column(
        String(25), nullable=True, default=None
    )
    disability_details: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, default=None
    )
    sibling_details: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, default=None
    )
    medical_details: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, default=None
    )

    # Defaulted Fields
    sibling_in_school: Mapped[bool] = mapped_column(Boolean, default=False)
    has_medical_condition: Mapped[bool] = mapped_column(Boolean, default=False)
    has_disability: Mapped[bool] = mapped_column(Boolean, default=False)
    is_transfer: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[StudentApplicationStatusEnum] = mapped_column(
        Enum(
            StudentApplicationStatusEnum,
            name="student_application_status_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=StudentApplicationStatusEnum.PENDING,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=True,
        default=None,
    )

    # Many-To-One Relationships
    grade: Mapped["Grade"] = relationship(
        "Grade",
        back_populates="students",
        repr=False,
        passive_deletes=True,
        init=False,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="student",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    mark_lists: Mapped[List["MarkList"]] = relationship(
        "MarkList",
        back_populates="student",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    term_records: Mapped[List["StudentTermRecord"]] = relationship(
        "StudentTermRecord",
        back_populates="student",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    subject_yearly_averages: Mapped[List["SubjectYearlyAverage"]] = relationship(
        "SubjectYearlyAverage",
        back_populates="student",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    assessments: Mapped[List["Assessment"]] = relationship(
        "Assessment",
        back_populates="student",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    years: Mapped[List["Year"]] = relationship(
        "Year",
        secondary="student_year_links",
        back_populates="students",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    academic_terms: Mapped[List["AcademicTerm"]] = relationship(
        "AcademicTerm",
        secondary="student_academic_term_links",
        back_populates="students",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    streams: Mapped[List["Stream"]] = relationship(
        "Stream",
        secondary="student_stream_links",
        back_populates="students",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    grades: Mapped[List["Grade"]] = relationship(
        "Grade",
        secondary="student_grade_links",
        back_populates="students",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    sections: Mapped[List["Section"]] = relationship(
        "Section",
        secondary="student_section_links",
        back_populates="students",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    subjects: Mapped[List["Subject"]] = relationship(
        "Subject",
        secondary="student_subject_links",
        back_populates="students",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
