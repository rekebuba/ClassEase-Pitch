#!/usr/bin/python3
"""Module for Assessment class"""

from typing import TYPE_CHECKING
from sqlalchemy import Integer, ForeignKey, Float
from models.base.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base.column_type import UUIDType
import uuid


if TYPE_CHECKING:
    from models.student import Student
    from models.student_term_record import StudentTermRecord
    from models.yearly_subject import YearlySubject


class Assessment(BaseModel):
    """
    This model represents an assessment record for a student including details
    """

    __tablename__ = "assessments"
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    student_term_record_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("student_term_records.id", ondelete="CASCADE"),
        nullable=False,
    )
    yearly_subject_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("yearly_subjects.id", ondelete="CASCADE"), nullable=False
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
