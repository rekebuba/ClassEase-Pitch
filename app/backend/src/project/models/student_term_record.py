#!/usr/bin/python3
"""Module for StudentTermRecord class"""

import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import UUID, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel

if TYPE_CHECKING:
    from project.models.academic_term import AcademicTerm
    from project.models.grade import Grade
    from project.models.mark_list import MarkList
    from project.models.section import Section
    from project.models.stream import Stream
    from project.models.student import Student


class StudentTermRecord(BaseModel):
    """
    This model represents the average result of a student
    for a particular term and year.
    """

    __tablename__ = "student_term_records"
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    academic_term_id: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("academic_terms.id", ondelete="CASCADE"), nullable=False
    )
    grade_id: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("grades.id", ondelete="CASCADE"), nullable=False
    )
    section_id: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("sections.id", ondelete="CASCADE"), nullable=False
    )
    stream_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("streams.id", ondelete="CASCADE"),
        nullable=True,
        default=None,
    )

    average: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    rank: Mapped[int] = mapped_column(Integer, nullable=True, default=None)

    # One-To-Many Relationships
    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="term_records",
        init=False,
    )
    academic_term: Mapped["AcademicTerm"] = relationship(
        "AcademicTerm",
        back_populates="student_term_records",
        init=False,
    )
    section: Mapped["Section"] = relationship(
        "Section",
        back_populates="student_term_records",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    grade: Mapped["Grade"] = relationship(
        "Grade",
        back_populates="student_term_records",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    stream: Mapped["Stream"] = relationship(
        "Stream",
        back_populates="student_term_records",
        init=False,
        repr=False,
        passive_deletes=True,
    )

    # Many-To-One Relationships
    mark_lists: Mapped[List["MarkList"]] = relationship(
        "MarkList",
        back_populates="student_term_record",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
