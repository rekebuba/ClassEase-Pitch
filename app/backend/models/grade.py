#!/usr/bin/python3
"""Module for Grade class"""

from sqlalchemy import Enum, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extension.enums.enum import GradeLevelEnum
from models.base.base_model import BaseModel
from typing import TYPE_CHECKING, List


from models.base.column_type import UUIDType
import uuid


if TYPE_CHECKING:
    from models.teacher_term_record import TeacherTermRecord
    from models.stream import Stream
    from models.student import Student
    from models.yearly_subject import YearlySubject
    from models.teacher import Teacher
    from models.section import Section
    from models.subject import Subject
    from models.year import Year


class Grade(BaseModel):
    """Grade Model"""

    __tablename__ = "grades"

    # Database column
    year_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("years.id"), nullable=False, index=True
    )
    grade: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
    level: Mapped[GradeLevelEnum] = mapped_column(
        Enum(
            GradeLevelEnum,
            name="grade_level_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )
    has_stream: Mapped[bool] = mapped_column(nullable=False, default=False)

    # One-To-Many Relationships
    year: Mapped["Year"] = relationship(
        "Year",
        back_populates="grades",
        repr=False,
        init=False,
    )

    # Many-To-One Relationships
    sections: Mapped[List["Section"]] = relationship(
        "Section",
        back_populates="grade",
        default_factory=list,
        repr=False,
    )
    streams: Mapped[List["Stream"]] = relationship(
        "Stream",
        back_populates="grade",
        default_factory=list,
        repr=False,
    )
    teacher_term_records: Mapped[List["TeacherTermRecord"]] = relationship(
        "TeacherTermRecord",
        back_populates="grade",
        default_factory=list,
        repr=False,
    )

    # Many-To-Many Relationships
    teachers: Mapped[List["Teacher"]] = relationship(
        "Teacher",
        back_populates="grades",
        secondary="teacher_grade_links",
        repr=False,
        default_factory=list,
    )
    yearly_subjects: Mapped[List["YearlySubject"]] = relationship(
        "YearlySubject",
        back_populates="grade",
        repr=False,
        default_factory=list,
    )
    subjects: Mapped[List["Subject"]] = relationship(
        "Subject",
        back_populates="grades",
        secondary="subject_grade_links",
        default_factory=list,
        repr=False,
    )
    students: Mapped[List["Student"]] = relationship(
        "Student",
        secondary="student_grade_links",
        back_populates="grades",
        default_factory=list,
        repr=False,
    )
