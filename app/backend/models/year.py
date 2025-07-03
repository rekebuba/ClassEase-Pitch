#!/usr/bin/python3
"""Module for Year class"""

from typing import TYPE_CHECKING, List
from sqlalchemy import String, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extension.enums.enum import AcademicTermTypeEnum
from models.base_model import BaseModel

if TYPE_CHECKING:
    from models.yearly_subject import YearlySubject
    from models.student_year_record import StudentYearRecord
    from models.event import Event
    from models.academic_term import AcademicTerm


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
    ethiopian_year: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    gregorian_year: Mapped[str] = mapped_column(
        String(15), default=None, nullable=True, unique=True
    )

    # Relationships
    student_year_records: Mapped[List["StudentYearRecord"]] = relationship(
        "StudentYearRecord",
        back_populates="year",
        default_factory=list,
        repr=False,
    )
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
