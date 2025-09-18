#!/usr/bin/python3
"""Module for TeacherRecord class"""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base.base_model import BaseModel
from models.base.column_type import UUIDType

if TYPE_CHECKING:
    from models.academic_term import AcademicTerm
    from models.employee import Employee
    from models.grade_stream_subject import GradeStreamSubject
    from models.subject import Subject
    from models.teacher_record_link import TeacherRecordLink


class TeacherRecord(BaseModel):
    __tablename__ = "teacher_records"
    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
    )
    academic_term_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("academic_terms.id", ondelete="CASCADE"),
        nullable=False,
    )
    grade_stream_subject_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUIDType(),
        ForeignKey("grade_stream_subjects.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )
    subject_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUIDType(),
        ForeignKey("subjects.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )

    __table_args__ = (
        UniqueConstraint(
            "employee_id",
            "academic_term_id",
            "subject_id",
            "grade_stream_subject_id",
            name="uq_teacher_record",
        ),
    )

    # Many-To-One Relationships
    teacher: Mapped["Employee"] = relationship(
        "Employee",
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
    subject: Mapped[Optional["Subject"]] = relationship(
        "Subject",
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
    teacher_record_links: Mapped[List["TeacherRecordLink"]] = relationship(
        "TeacherRecordLink",
        back_populates="teacher_record",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
