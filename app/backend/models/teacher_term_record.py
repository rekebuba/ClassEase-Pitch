#!/usr/bin/python3
"""Module for TeacherTermRecord class"""

from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from models.base.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base.column_type import UUIDType
import uuid


if TYPE_CHECKING:
    from models.academic_term import AcademicTerm
    from models.teacher import Teacher
    from models.grade import Grade
    from models.section import Section
    from models.stream import Stream
    from models.subject import Subject


class TeacherTermRecord(BaseModel):
    __tablename__ = "teacher_term_records"
    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("teachers.id"), nullable=False
    )
    academic_term_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("academic_terms.id"), nullable=False
    )
    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("subjects.id"), nullable=False
    )
    grade_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("grades.id"), nullable=False
    )
    section_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("sections.id"), nullable=False
    )
    stream_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("streams.id"), nullable=True, default=None
    )

    # One-To-Many Relationships
    teacher: Mapped["Teacher"] = relationship(
        "Teacher",
        back_populates="term_records",
        init=False,
        repr=False,
    )
    academic_term: Mapped["AcademicTerm"] = relationship(
        "AcademicTerm",
        back_populates="teacher_term_records",
        init=False,
        repr=False,
    )
    subject: Mapped["Subject"] = relationship(
        "Subject",
        back_populates="teacher_term_records",
        init=False,
        repr=False,
    )
    section: Mapped["Section"] = relationship(
        "Section",
        back_populates="teacher_term_records",
        init=False,
        repr=False,
    )
    grade: Mapped["Grade"] = relationship(
        "Grade",
        back_populates="teacher_term_records",
        init=False,
        repr=False,
    )
    stream: Mapped["Stream"] = relationship(
        "Stream",
        back_populates="teacher_term_records",
        init=False,
        repr=False,
    )
