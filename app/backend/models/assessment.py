#!/usr/bin/python3
"""Module for Assessment class"""

from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, Float
from models.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.student import Student
    from models.student_semester_record import StudentSemesterRecord
    from models.yearly_subject import YearlySubject


class Assessment(BaseModel):
    """
    This model represents an assessment record for a student, including details such as the student's ID, grade ID, subject ID, total score, rank, semester, and year.
    """

    __tablename__ = "assessments"
    student_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("students.id"), nullable=False
    )
    student_semester_record_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("student_semester_records.id"), nullable=False
    )
    yearly_subject_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("yearly_subjects.id"), nullable=False
    )
    teachers_record_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("teachers_records.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )
    # The subject sum score of the student for each assessment
    total: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    rank: Mapped[int] = mapped_column(Integer, nullable=True, default=None)

    # Relationship
    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="assessments",
        init=False,
        repr=False,
    )
    student_semester_record: Mapped["StudentSemesterRecord"] = relationship(
        "StudentSemesterRecord",
        back_populates="assessments",
        init=False,
        repr=False,
    )
    yearly_subject: Mapped["YearlySubject"] = relationship(
        "YearlySubject",
        back_populates="assessments",
        init=False,
        repr=False,
    )
