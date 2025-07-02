#!/usr/bin/python3
"""Module for Year class"""

from typing import TYPE_CHECKING, List
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, scoped_session, Session
from extension.functions.helper import current_EC_year, current_GC_year, academic_year
from models.base_model import BaseModel

if TYPE_CHECKING:
    from models.yearly_subject import YearlySubject
    from models.student_year_record import StudentYearRecord
    from models.event import Event
    from models.semester import Semester


def seed_year(session: scoped_session[Session]) -> None:
    # Check if the table is already populated
    if session.query(Year).count() > 0:
        return

    ethiopian_year = current_EC_year()
    gregorian_year = current_GC_year(ethiopian_year)

    new_year = Year(
        academic_year=academic_year(ethiopian_year),
        ethiopian_year=ethiopian_year,
        gregorian_year=gregorian_year,
    )

    session.add(new_year)
    session.commit()


class Year(BaseModel):
    """docstring for year."""

    __tablename__ = "years"
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
    semesters: Mapped[List["Semester"]] = relationship(
        "Semester",
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
