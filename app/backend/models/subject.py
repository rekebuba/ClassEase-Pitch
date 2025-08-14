#!/usr/bin/python3
"""Module for Subject class"""

from typing import TYPE_CHECKING, List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base.base_model import BaseModel
from models.base.column_type import UUIDType
import uuid



if TYPE_CHECKING:
    from models.grade_stream_subject import GradeStreamSubject
    from models.teacher_term_record import TeacherTermRecord
    from models.mark_list import MarkList
    from models.teacher import Teacher
    from models.year import Year
    from models.grade import Grade
    from models.stream import Stream
    from models.yearly_subject import YearlySubject
    from models.student import Student


class Subject(BaseModel):
    """
    Subject Model
    """

    __tablename__ = "subjects"
    year_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("years.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    code: Mapped[str] = mapped_column(String(25), nullable=False)

    # One-To-Many Relationships
    year: Mapped["Year"] = relationship(
        "Year",
        back_populates="subjects",
        repr=False,
        passive_deletes=True,
        init=False,
    )

    # Many-To-One Relationships
    teacher_term_records: Mapped[List["TeacherTermRecord"]] = relationship(
        "TeacherTermRecord",
        back_populates="subject",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    grade_stream_subjects: Mapped[List["GradeStreamSubject"]] = relationship(
        "GradeStreamSubject",
        back_populates="subject",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    # Many-To-Many Relationships
    teachers: Mapped[List["Teacher"]] = relationship(
        "Teacher",
        back_populates="subjects",
        secondary="teacher_subject_links",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    yearly_subjects: Mapped[List["YearlySubject"]] = relationship(
        "YearlySubject",
        back_populates="subject",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    grades: Mapped[List["Grade"]] = relationship(
        "Grade",
        secondary="subject_grade_links",
        back_populates="subjects",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    streams: Mapped[List["Stream"]] = relationship(
        "Stream",
        secondary="subject_stream_links",
        back_populates="subjects",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    students: Mapped[List["Student"]] = relationship(
        "Student",
        secondary="student_subject_links",
        back_populates="subjects",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    mark_lists: Mapped[List["MarkList"]] = relationship(
        "MarkList",
        back_populates="subject",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
