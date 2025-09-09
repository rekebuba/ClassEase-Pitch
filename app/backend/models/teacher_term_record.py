#!/usr/bin/python3
"""Module for TeacherTermRecord class"""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base.base_model import BaseModel
from models.base.column_type import UUIDType

if TYPE_CHECKING:
    from models.academic_term import AcademicTerm
    from models.grade import Grade
    from models.section import Section
    from models.stream import Stream
    from models.subject import Subject
    from models.teacher import Teacher


class TeacherTermRecord(BaseModel):
    __tablename__ = "teacher_term_records"
    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False
    )
    academic_term_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("academic_terms.id", ondelete="CASCADE"), nullable=False
    )
    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
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

    # One-To-Many Relationships
    teacher: Mapped["Teacher"] = relationship(
        "Teacher",
        back_populates="term_records",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    academic_term: Mapped["AcademicTerm"] = relationship(
        "AcademicTerm",
        back_populates="teacher_term_records",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    subject: Mapped["Subject"] = relationship(
        "Subject",
        back_populates="teacher_term_records",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    section: Mapped["Section"] = relationship(
        "Section",
        back_populates="teacher_term_records",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    grade: Mapped["Grade"] = relationship(
        "Grade",
        back_populates="teacher_term_records",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    stream: Mapped["Stream"] = relationship(
        "Stream",
        back_populates="teacher_term_records",
        init=False,
        repr=False,
        passive_deletes=True,
    )
