#!/usr/bin/python3
"""Module for Student class"""

from typing import TYPE_CHECKING
from sqlalchemy import (
    Date,
    String,
    ForeignKey,
    Boolean,
    Text,
)
from models.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.stud_semester_record import STUDSemesterRecord
    from models.stud_year_record import STUDYearRecord
    from models.average_subject import AVRGSubject
    from models.user import User


class Student(BaseModel):
    """
    Represents a student entity in the database.
    """

    __tablename__ = "students"
    user_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("users.id"), unique=True, nullable=False
    )
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    father_name: Mapped[str] = mapped_column(String(50), nullable=False)
    grand_father_name: Mapped[str] = mapped_column(String(50), nullable=False)
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(1), nullable=False)

    # Parent/Guardian Contacts
    father_phone: Mapped[str] = mapped_column(String(25))
    mother_phone: Mapped[str] = mapped_column(String(25))
    guardian_name: Mapped[str] = mapped_column(
        String(50)
    )  # If student lives with someone else
    guardian_phone: Mapped[str] = mapped_column(String(25))

    # Academic Info
    start_year_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("years.id"), nullable=False
    )
    current_year_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("years.id"), nullable=False
    )
    current_grade_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("grades.id"), nullable=False
    )
    next_grade_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("grades.id"), nullable=True, default=None
    )
    semester_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("semesters.id"), nullable=True, default=None
    )
    has_passed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_registered: Mapped[bool] = mapped_column(Boolean, default=False)

    # If transferring from another school
    is_transfer: Mapped[bool] = mapped_column(Boolean, default=False)
    previous_school_name: Mapped[str] = mapped_column(
        String(100), nullable=True, default=None
    )

    # Identification & Legal Docs
    birth_certificate: Mapped[str] = mapped_column(
        String(255), nullable=True, default=None
    )  # Path to uploaded file

    # Health & Special Needs
    has_medical_condition: Mapped[bool] = mapped_column(Boolean, default=False)
    # Explanation of medical conditions
    medical_details: Mapped[str] = mapped_column(Text, nullable=True, default=None)
    has_disability: Mapped[bool] = mapped_column(Boolean, default=False)
    # Explanation of disabilities
    disability_details: Mapped[str] = mapped_column(Text, nullable=True, default=None)
    requires_special_accommodation: Mapped[bool] = mapped_column(Boolean, default=False)
    special_accommodation_details: Mapped[str] = mapped_column(
        Text, nullable=True, default=None
    )  # Any special support needed

    # Whether the student is currently enrolled
    is_active: bool = False

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="students",
        init=False,
    )
    semester_records: Mapped[list["STUDSemesterRecord"]] = relationship(
        "STUDSemesterRecord",
        back_populates="students",
        cascade="all, delete-orphan",
        uselist=False,
        init=False,
    )
    year_records: Mapped[list["STUDYearRecord"]] = relationship(
        "STUDYearRecord",
        back_populates="students",
        cascade="all, delete-orphan",
        uselist=False,
        init=False,
    )
    average_subjects: Mapped[list["AVRGSubject"]] = relationship(
        "AVRGSubject",
        back_populates="students",
        cascade="all, delete-orphan",
        init=False,
    )
