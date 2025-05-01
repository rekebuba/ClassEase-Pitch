#!/usr/bin/python3
""" Module for STUDYearRecord class """

from sqlalchemy import Integer, String, ForeignKey, CheckConstraint, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel


class STUDYearRecord(BaseModel):
    """
    Represents a student's yearly academic record.
    """
    __tablename__ = 'student_year_records'
    user_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('users.id'), nullable=False)
    student_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('students.id'), nullable=False)
    grade_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('grades.id'), nullable=False)
    year_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('years.id'), nullable=False)
    final_score: Mapped[float] = mapped_column(
        Float, nullable=True, default=None)  # year-end score
    rank: Mapped[int] = mapped_column(Integer, nullable=True, default=None)

    # Relationships
    student = relationship("Student", back_populates='student_year_record', uselist=False)
