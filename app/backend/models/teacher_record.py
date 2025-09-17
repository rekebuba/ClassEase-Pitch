#!/usr/bin/python3
"""Module for TeacherRecord class"""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base.base_model import BaseModel
from models.base.column_type import UUIDType

if TYPE_CHECKING:
    from models.academic_term import AcademicTerm
    from models.grade_stream_subject import GradeStreamSubject
    from models.section import Section
    from models.teacher import Teacher


class TeacherRecord(BaseModel):
    __tablename__ = "teacher_records"
    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False
    )
    academic_term_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("academic_terms.id", ondelete="CASCADE"), nullable=False
    )
    grade_stream_subject_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("grade_stream_subjects.id", ondelete="CASCADE"),
        nullable=False,
    )
    section_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("sections.id", ondelete="CASCADE"), nullable=False
    )

    __table_args__ = UniqueConstraint(
        "teacher_id",
        "academic_term_id",
        "grade_stream_subject_id",
        "section_id",
        name="uq_teacher_record",
    )

    # Many-To-One Relationships
    teacher: Mapped["Teacher"] = relationship(
        "Teacher",
        back_populates="teacher_records",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    academic_term: Mapped["AcademicTerm"] = relationship(
        "AcademicTerm",
        back_populates="teacher_records",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    grade_stream_subject: Mapped["GradeStreamSubject"] = relationship(
        "GradeStreamSubject",
        back_populates="teacher_records",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    section: Mapped["Section"] = relationship(
        "Section",
        back_populates="teacher_records",
        init=False,
        repr=False,
        passive_deletes=True,
    )
