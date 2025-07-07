#!/usr/bin/python3
"""Module for Student class"""

from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import (
    Date,
    String,
    ForeignKey,
    Boolean,
    Text,
    Enum,
)
from models.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extension.enums.enum import GenderEnum, StudentApplicationStatusEnum

if TYPE_CHECKING:
    from models.grade import Grade
    from models.student_term_record import StudentTermRecord
    from models.student_year_record import StudentYearRecord
    from models.subject_yearly_average import SubjectYearlyAverage
    from models.user import User
    from models.assessment import Assessment


class Student(BaseModel):
    """
    Represents a student entity in the database.
    """

    __tablename__ = "students"

    # Personal Information
    starting_grade_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("grades.id"), nullable=False
    )
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
    father_phone: Mapped[str] = mapped_column(String(25))
    mother_phone: Mapped[str] = mapped_column(String(25))
    parent_email: Mapped[str] = mapped_column(String(120), nullable=False)

    grand_father_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    nationality: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    blood_type: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    student_photo: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    previous_school: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    previous_grades: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    transportation: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    guardian_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    guardian_phone: Mapped[Optional[str]] = mapped_column(String(25), nullable=True)
    guardian_relation: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    emergency_contact_name: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True
    )
    emergency_contact_phone: Mapped[Optional[str]] = mapped_column(
        String(25), nullable=True
    )
    disability_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sibling_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    medical_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

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

    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id"),
        unique=True,
        nullable=True,
        default=None,
    )

    # Relationships
    starting_grade: Mapped["Grade"] = relationship(
        "Grade",
        back_populates="students",
        init=False,
        repr=False,
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="students",
        init=False,
        repr=False,
    )
    student_term_records: Mapped[List["StudentTermRecord"]] = relationship(
        "StudentTermRecord",
        back_populates="student",
        default_factory=list,
        repr=False,
    )
    student_year_records: Mapped[List["StudentYearRecord"]] = relationship(
        "StudentYearRecord",
        back_populates="student",
        default_factory=list,
        repr=False,
    )
    subject_yearly_averages: Mapped[List["SubjectYearlyAverage"]] = relationship(
        "SubjectYearlyAverage",
        back_populates="student",
        default_factory=list,
        repr=False,
    )
    assessments: Mapped[List["Assessment"]] = relationship(
        "Assessment",
        back_populates="student",
        default_factory=list,
        repr=False,
    )
