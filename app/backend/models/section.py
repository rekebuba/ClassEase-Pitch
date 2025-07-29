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
    from models.teacher_term_record import TeacherTermRecord
    from models.grade import Grade
    from models.student import Student
    from models.teacher import Teacher


class Section(BaseModel):
    """
    Represents a section within a grade.
    """

    __tablename__ = "sections"
    grade_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("grades.id"), nullable=False
    )
    section: Mapped[str] = mapped_column(
        String(1), nullable=True, default=None
    )  # e.g., A, B, C, D, E, F, G

    # Relationships
    grade: Mapped["Grade"] = relationship(
        "Grade",
        back_populates="sections",
        repr=False,
        init=False,
    )

    # Many-To-One Relationships
    teacher_term_records: Mapped[List["TeacherTermRecord"]] = relationship(
        "TeacherTermRecord",
        back_populates="section",
        default_factory=list,
        repr=False,
    )
    student_term_records: Mapped[List["StudentTermRecord"]] = relationship(
        "StudentTermRecord",
        back_populates="section",
        default_factory=list,
        repr=False,
    )

    # Many-to-many relationships
    teachers: Mapped[List["Teacher"]] = relationship(
        "Teacher",
        back_populates="sections",
        secondary="teacher_section_links",
        default_factory=list,
        repr=False,
    )

    students: Mapped[List["Student"]] = relationship(
        "Student",
        secondary="student_section_links",
        back_populates="sections",
        default_factory=list,
        repr=False,
    )
