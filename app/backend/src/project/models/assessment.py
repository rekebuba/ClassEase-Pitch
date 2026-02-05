#!/usr/bin/python3
"""Module for Assessment class"""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel

if TYPE_CHECKING:
    from project.models.student import Student
    from project.models.yearly_subject import YearlySubject


class Assessment(BaseModel):
    """
    This model represents an assessment record for a student including details
    """

    __tablename__ = "assessments"
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    student_term_record_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("student_term_records.id", ondelete="CASCADE"),
        nullable=False,
    )
    yearly_subject_id: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("yearly_subjects.id", ondelete="CASCADE"), nullable=False
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
        passive_deletes=True,
    )
    yearly_subject: Mapped["YearlySubject"] = relationship(
        "YearlySubject",
        back_populates="assessments",
        init=False,
        repr=False,
        passive_deletes=True,
    )
