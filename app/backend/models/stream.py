#!/usr/bin/python3
"""Module for Subject class"""

import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base.base_model import BaseModel
from sqlalchemy import UUID

if TYPE_CHECKING:
    from models.grade import Grade
    from models.grade_stream_subject import GradeStreamSubject
    from models.student import Student
    from models.student_term_record import StudentTermRecord
    from models.subject import Subject


class Stream(BaseModel):
    __tablename__ = "streams"

    grade_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("grades.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    __table_args__ = (UniqueConstraint("grade_id", "name", name="uq_grade_name"),)

    # One-To-Many Relationships
    grade: Mapped["Grade"] = relationship(
        "Grade",
        back_populates="streams",
        repr=False,
        passive_deletes=True,
        init=False,
    )

    # Many-To-One Relationships
    student_term_records: Mapped[List["StudentTermRecord"]] = relationship(
        "StudentTermRecord",
        back_populates="stream",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    # Many-To-Many Relationships
    students: Mapped[List["Student"]] = relationship(
        "Student",
        secondary="student_stream_links",
        back_populates="streams",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    # Association Object
    grade_stream_subjects: Mapped[List["GradeStreamSubject"]] = relationship(
        "GradeStreamSubject",
        back_populates="stream",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    # Association proxy
    subjects: AssociationProxy[List["Subject"]] = association_proxy(
        "grade_stream_subjects",
        "subject",
        default_factory=list,
    )
