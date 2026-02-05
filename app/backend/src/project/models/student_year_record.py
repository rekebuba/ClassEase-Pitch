#!/usr/bin/python3
"""Module for StudentYearRecord class"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import UUID, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from project.models.base.base_model import BaseModel

if TYPE_CHECKING:
    pass


class StudentYearRecord(BaseModel):
    """
    Represents a student's yearly academic record.
    """

    __tablename__ = "student_year_records"
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    grade_id: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("grades.id", ondelete="CASCADE"), nullable=False
    )
    year_id: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("years.id", ondelete="CASCADE"), nullable=False
    )
    stream_id: Mapped[Optional[str]] = mapped_column(
        UUID(),
        ForeignKey("streams.id", ondelete="CASCADE"),
        nullable=True,
        default=None,
    )
    final_score: Mapped[float] = mapped_column(
        Float, nullable=True, default=None
    )  # year-end score
    rank: Mapped[int] = mapped_column(Integer, nullable=True, default=None)
