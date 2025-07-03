#!/usr/bin/python3
"""Module for StudentYearRecord class"""

from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Integer, String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel

if TYPE_CHECKING:
    from models.grade import Grade
    from models.subject_yearly_average import SubjectYearlyAverage
    from models.student_term_record import StudentTermRecord
    from models.student import Student
    from models.year import Year
    from models.stream import Stream


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
    stream_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("streams.id"),
        nullable=True,
        default=None,
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
        repr=False,
    )
    grade: Mapped["Grade"] = relationship(
        "Grade",
        back_populates="student_year_records",
        init=False,
        repr=False,
    )
    year: Mapped["Year"] = relationship(
        "Year",
        back_populates="student_year_records",
        init=False,
        repr=False,
    )
    student_term_records: Mapped[List["StudentTermRecord"]] = relationship(
        "StudentTermRecord",
        back_populates="student_year_record",
        default_factory=list,
        repr=False,
    )
    stream: Mapped[Optional["Stream"]] = relationship(
        "Stream",
        back_populates="students",
        init=False,
        repr=False,
    )
    subject_yearly_averages: Mapped[List["SubjectYearlyAverage"]] = relationship(
        "SubjectYearlyAverage",
        back_populates="student_year_record",
        default_factory=list,
        repr=False,
    )
