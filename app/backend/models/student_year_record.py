#!/usr/bin/python3
"""Module for StudentYearRecord class"""

from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base.base_model import BaseModel

from models.base.column_type import UUIDType
import uuid
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
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("students.id", ondelete='CASCADE'), nullable=False
    )
    grade_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("grades.id", ondelete='CASCADE'), nullable=False
    )
    year_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("years.id", ondelete='CASCADE'), nullable=False
    )
    stream_id: Mapped[Optional[str]] = mapped_column(
        UUIDType(),
        ForeignKey("streams.id", ondelete='CASCADE'),
        nullable=True,
        default=None,
    )
    final_score: Mapped[float] = mapped_column(
        Float, nullable=True, default=None
    )  # year-end score
    rank: Mapped[int] = mapped_column(Integer, nullable=True, default=None)
