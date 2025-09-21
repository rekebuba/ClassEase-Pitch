#!/usr/bin/python3
"""Module for Section class"""

import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base.base_model import BaseModel
from models.base.column_type import UUIDType

if TYPE_CHECKING:
    from models.grade import Grade
    from models.student import Student
    from models.student_term_record import StudentTermRecord
    from models.teacher_record import TeacherRecord


class Section(BaseModel):
    """
    Represents a section within a grade.
    """

    __tablename__ = "sections"
    grade_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("grades.id", ondelete="CASCADE"),
        nullable=False,
    )
    section: Mapped[str] = mapped_column(
        String(1),
        nullable=True,
    )  # e.g., A, B, C, D, E, F, G

    # Relationships
    grade: Mapped["Grade"] = relationship(
        "Grade",
        back_populates="sections",
        repr=False,
        passive_deletes=True,
        init=False,
    )

    # Many-To-One Relationships
    student_term_records: Mapped[List["StudentTermRecord"]] = relationship(
        "StudentTermRecord",
        back_populates="section",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    # Many-to-many relationships
    teacher_records: Mapped[List["TeacherRecord"]] = relationship(
        "TeacherRecord",
        back_populates="section",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    students: Mapped[List["Student"]] = relationship(
        "Student",
        secondary="student_section_links",
        back_populates="sections",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
