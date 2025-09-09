#!/usr/bin/python3
"""Module for StudentTermRecord class"""

from typing import TYPE_CHECKING, List
from sqlalchemy import Integer, ForeignKey, Float
from models.base.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base.column_type import UUIDType
import uuid


if TYPE_CHECKING:
    from models.grade import Grade
    from models.mark_list import MarkList
    from models.section import Section
    from models.stream import Stream
    from models.academic_term import AcademicTerm
    from models.student import Student


class StudentTermRecord(BaseModel):
    """
    This model represents the average result of a student for a particular term and year.
    """

    __tablename__ = "student_term_records"
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    academic_term_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("academic_terms.id", ondelete="CASCADE"), nullable=False
    )
    grade_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("grades.id", ondelete="CASCADE"), nullable=False
    )
    section_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("sections.id", ondelete="CASCADE"), nullable=False
    )
    stream_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
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
