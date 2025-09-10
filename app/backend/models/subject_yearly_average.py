#!/usr/bin/python3
"""Module for SubjectYearlyAverage class"""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base.base_model import BaseModel
from models.base.column_type import UUIDType

if TYPE_CHECKING:
    from models.student import Student
    from models.student_year_record import StudentYearRecord
    from models.yearly_subject import YearlySubject


class SubjectYearlyAverage(BaseModel):
    __tablename__ = "subject_yearly_averages"
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    yearly_subject_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("yearly_subjects.id", ondelete="CASCADE"), nullable=False
    )
    student_year_record_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("student_year_records.id", ondelete="CASCADE"),
        nullable=True,
    )
    # The actual average score of the student in this for all subject
    average: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    rank: Mapped[int] = mapped_column(Integer, nullable=True, default=None)

    # Relationships
    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="subject_yearly_averages",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    yearly_subject: Mapped["YearlySubject"] = relationship(
        "YearlySubject",
        back_populates="subject_yearly_averages",
        init=False,
        repr=False,
        passive_deletes=True,
    )
