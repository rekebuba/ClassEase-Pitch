#!/usr/bin/python3
"""Module for STUDYearRecord class"""

from sqlalchemy import Integer, String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel


class STUDYearRecord(BaseModel):
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
    students = relationship("Student", back_populates="year_records")
    grades = relationship("Grade", back_populates="student_year_records")
    years = relationship("Year", back_populates="student_year_records")
    semester_records = relationship("STUDSemesterRecord", back_populates="year_records")
