#!/usr/bin/python3
"""Module for Year class"""

from typing import TYPE_CHECKING, List
from sqlalchemy import Date, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extension.enums.enum import AcademicTermTypeEnum, AcademicYearStatusEnum
from models.base.base_model import BaseModel

if TYPE_CHECKING:
    from models.yearly_subject import YearlySubject
    from models.event import Event
    from models.academic_term import AcademicTerm
    from models.grade import Grade
    from models.section import Section
    from models.stream import Stream
    from models.subject import Subject
    from models.student import Student
    from models.teacher import Teacher


class Year(BaseModel):
    """docstring for year."""

    __tablename__ = "years"

    calendar_type: Mapped[AcademicTermTypeEnum] = mapped_column(
        Enum(
            AcademicTermTypeEnum,
            name="term_type_enum",
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
    )

    academic_year: Mapped[str] = mapped_column(String(50), unique=True)
    ethiopian_year: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)
    gregorian_year: Mapped[str] = mapped_column(String(15), nullable=True, unique=True)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(
        Enum(
            AcademicYearStatusEnum,
            name="year_status_enum",
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
    )

    # Relationships
    events: Mapped[List["Event"]] = relationship(
        "Event",
        back_populates="year",
        default_factory=list,
        repr=False,
    )
    academic_terms: Mapped[List["AcademicTerm"]] = relationship(
        "AcademicTerm",
        back_populates="year",
        default_factory=list,
        repr=False,
    )
    yearly_subjects: Mapped[List["YearlySubject"]] = relationship(
        "YearlySubject",
        back_populates="year",
        repr=False,
        default_factory=list,
    )
    grades: Mapped[List["Grade"]] = relationship(
        "Grade",
        back_populates="year",
        repr=False,
        default_factory=list,
    )
    subjects: Mapped[List["Subject"]] = relationship(
        "Subject",
        back_populates="year",
        repr=False,
        default_factory=list,
    )

    students: Mapped[List["Student"]] = relationship(
        "Student",
        secondary="student_year_links",
        back_populates="years",
        default_factory=list,
        repr=False,
    )
    teachers: Mapped[List["Teacher"]] = relationship(
        "Teacher",
        secondary="teacher_year_links",
        back_populates="years",
        default_factory=list,
        repr=False,
    )
