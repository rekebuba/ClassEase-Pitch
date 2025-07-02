#!/usr/bin/python3
"""Module for StudentYearRecord class"""

from typing import TYPE_CHECKING, List
from sqlalchemy import Integer, String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel

if TYPE_CHECKING:
    from models.subject import Subject
    from models.grade import Grade
    from models.student_semester_record import StudentSemesterRecord
    from models.student import Student
    from models.year import Year


class StudentYearRecord(BaseModel):
    """
    Represents a student's yearly academic record.
    """

    __tablename__ = "student_year_records"
    student_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("students.id"), nullable=False
    )
    grade_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("grades.id"), nullable=False
    )
    year_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("years.id"), nullable=False
    )
    final_score: Mapped[float] = mapped_column(
        Float, nullable=True, default=None
    )  # year-end score
    rank: Mapped[int] = mapped_column(Integer, nullable=True, default=None)

    # Relationships
    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="student_year_records",
        init=False,
    )
    grade: Mapped["Grade"] = relationship(
        "Grade",
        back_populates="student_year_records",
        init=False,
    )
    year: Mapped["Year"] = relationship(
        "Year",
        back_populates="student_year_records",
        init=False,
    )
    student_semester_records: Mapped[List["StudentSemesterRecord"]] = relationship(
        "StudentSemesterRecord",
        back_populates="student_year_record",
        default_factory=list,
        repr=False,
    )
