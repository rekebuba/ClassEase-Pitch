#!/usr/bin/python3
"""Module for Section class"""

from typing import TYPE_CHECKING, List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel

if TYPE_CHECKING:
    from models.student_term_record import StudentTermRecord
    from models.teacher_record import TeachersRecord


class Section(BaseModel):
    """
    Represents a section within a grade.
    """

    __tablename__ = "sections"
    section: Mapped[str] = mapped_column(
        String(1), nullable=True, default=None
    )  # e.g., A, B, C, D, E, F, G

    # Relationships
    student_term_records: Mapped[List["StudentTermRecord"]] = relationship(
        "StudentTermRecord",
        back_populates="section",
        default_factory=list,
        repr=False,
    )

    # Many-to-many relationships
    teacher_records_link: Mapped[List["TeachersRecord"]] = relationship(
        "TeachersRecord",
        back_populates="sections_link",
        secondary="teacher_record_section_links",
        default_factory=list,
        repr=False,
    )
