#!/usr/bin/python3
"""Module for Year class"""

from datetime import date
from typing import TYPE_CHECKING, List

from sqlalchemy import Date, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base.base_model import BaseModel
from utils.enum import AcademicTermTypeEnum, AcademicYearStatusEnum

if TYPE_CHECKING:
    from models.academic_term import AcademicTerm
    from models.event import Event
    from models.grade import Grade
    from models.student import Student
    from models.subject import Subject


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

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
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
        passive_deletes=True,
    )
    academic_terms: Mapped[List["AcademicTerm"]] = relationship(
        "AcademicTerm",
        back_populates="year",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    grades: Mapped[List["Grade"]] = relationship(
        "Grade",
        back_populates="year",
        repr=False,
        passive_deletes=True,
        default_factory=list,
    )
    subjects: Mapped[List["Subject"]] = relationship(
        "Subject",
        back_populates="year",
        repr=False,
        passive_deletes=True,
        default_factory=list,
    )

    students: Mapped[List["Student"]] = relationship(
        "Student",
        secondary="student_year_links",
        back_populates="years",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
