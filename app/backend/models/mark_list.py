#!/usr/bin/python3
"""Module for MarkList class"""

from sqlalchemy import String, Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column
from models.base_model import BaseModel


class MarkList(BaseModel):
    """
    This model represents a list of marks for students in various assessments. It includes details about the student, grade, section, subject, teacher's record, semester, year, type of assessment, percentage contribution to the final score, and the actual score obtained.
    """

    __tablename__ = "mark_lists"

    user_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("users.id"), nullable=False
    )
    student_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("students.id"), nullable=False
    )
    subject_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("subjects.id"), nullable=False
    )
    # e.g., 'Test', 'Quiz', 'Assignment', 'Midterm', 'Final'
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    percentage: Mapped[int] = mapped_column(Integer, nullable=False)
    score = mapped_column(Float, nullable=True, default=None)
    semester_record_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("student_semester_records.id"), nullable=False
    )
    teachers_record_id: Mapped[str] = mapped_column(
        String(120),
        ForeignKey("teachers_records.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )
