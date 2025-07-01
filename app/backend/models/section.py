#!/usr/bin/python3
"""Module for Section class"""

from typing import TYPE_CHECKING, List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel

if TYPE_CHECKING:
    from models.grade import Grade
    from models.student_semester_record import StudentSemesterRecord


class Section(BaseModel):
    """
    Represents a section within a grade.
    """

    __tablename__ = "sections"
    grade_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("grades.id"), nullable=False
    )
    section: Mapped[str] = mapped_column(
        String(1), nullable=True, default=None
    )  # e.g., A, B, C, D, E, F, G

    # Relationships
    grade: Mapped["Grade"] = relationship(
        "Grade", back_populates="sections", init=False
    )
    semester_records: Mapped[List["StudentSemesterRecord"]] = relationship(
        "StudentSemesterRecord", back_populates="sections", init=False
    )
