#!/usr/bin/python3
"""Module for SubjectYearlyAverage class"""

from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, Float
from models.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.student import Student


class SubjectYearlyAverage(BaseModel):
    __tablename__ = "subject_yearly_averages"
    student_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("students.id"), nullable=False
    )
    yearly_subject_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("yearly_subjects.id"), nullable=False
    )
    student_year_record_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("student_year_records.id"), nullable=True
    )
    # The actual average score of the student in this for all subject
    average: Mapped[float] = mapped_column(Float, default=None)
    rank: Mapped[int] = mapped_column(Integer, default=None)

    # Relationships
    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="subject_yearly_averages",
        default=None,
        repr=False,
    )
