#!/usr/bin/python3
"""Module for Section class"""

from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base.base_model import BaseModel

from models.base.column_type import UUIDType
import uuid
if TYPE_CHECKING:
    from models.student_term_record import StudentTermRecord
    from models.teacher_record import TeachersRecord
    from models.grade import Grade
    from models.year import Year


class Section(BaseModel):
    """
    Represents a section within a grade.
    """

    __tablename__ = "sections"
    year_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("years.id"), nullable=False, index=True
    )
    section: Mapped[str] = mapped_column(
        String(1), nullable=True, default=None
    )  # e.g., A, B, C, D, E, F, G

    # Relationships
    year: Mapped["Year"] = relationship(
        "Year",
        back_populates="sections",
        repr=False,
        init=False,
    )
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
    grades_link: Mapped[List["Grade"]] = relationship(
        "Grade",
        back_populates="sections_link",
        secondary="grade_section_links",
        default_factory=list,
        repr=False,
    )
