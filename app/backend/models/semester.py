#!/usr/bin/python3
"""Module for Semester class"""

from datetime import date
from typing import TYPE_CHECKING, List
from sqlalchemy import String, Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel
import sqlalchemy as sa


if TYPE_CHECKING:
    from models.student_semester_record import StudentSemesterRecord
    from models.year import Year


class Semester(BaseModel):
    """docstring for Semester."""

    __tablename__ = "semesters"
    year_id: Mapped[str] = mapped_column(
        String(125), ForeignKey("years.id"), nullable=False
    )
    name: Mapped[int] = mapped_column(Integer, nullable=False)

    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    registration_start: Mapped[date] = mapped_column(Date, nullable=True)
    registration_end: Mapped[date] = mapped_column(Date, nullable=True)

    # Relationships
    year: Mapped["Year"] = relationship(
        "Year",
        back_populates="semesters",
        init=False,
    )
    student_semester_records: Mapped[List["StudentSemesterRecord"]] = relationship(
        "StudentSemesterRecord",
        back_populates="semester",
        default_factory=list,
        repr=False,
    )

    __table_args__ = (
        sa.CheckConstraint("start_date <= end_date", name="check_semester_dates"),
        sa.CheckConstraint(
            "registration_start <= registration_end",
            name="check_semester_registration_dates",
        ),
    )
