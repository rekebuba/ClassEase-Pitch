#!/usr/bin/python3
"""Module for Section class"""

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel


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
    grade = relationship("Grade", back_populates="sections")
    semester_records = relationship(
        "STUDSemesterRecord", back_populates="sections", uselist=False
    )
