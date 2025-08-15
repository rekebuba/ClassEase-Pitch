#!/usr/bin/python3
"""Module for Subject class"""

from typing import TYPE_CHECKING, List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy
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

    # Association Object
    grade_stream_subjects: Mapped[List["GradeStreamSubject"]] = relationship(
        "GradeStreamSubject",
        back_populates="subject",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    # Association proxy
    _grades: AssociationProxy[List["Grade"]] = association_proxy(
        "grade_stream_subjects",
        "grade",
        default_factory=list,
    )
    _streams: AssociationProxy[List["Stream"]] = association_proxy(
        "grade_stream_subjects",
        "stream",
        default_factory=list,
    )

    @property
    def grades(self) -> List["Grade"]:
        """Return unique, non-null grades."""
        seen = set()
        result = []
        for g in self._grades:
            if g is not None and g.id not in seen:
                seen.add(g.id)
                result.append(g)
        return result

    @property
    def streams(self) -> List["Stream"]:
        """Return unique, non-null streams."""
        seen = set()
        result = []
        for s in self._streams:
            if s is not None and s.id not in seen:
                seen.add(s.id)
                result.append(s)
        return result
