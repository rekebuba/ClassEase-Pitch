#!/usr/bin/python3
"""Module for Subject class"""

import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, String
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base.base_model import BaseModel
from models.base.column_type import UUIDType
from models.grade import Grade
from models.stream import Stream
from models.teacher_record import TeacherRecord
from utils.utils import sort_grade_key

if TYPE_CHECKING:
    from models.grade_stream_subject import GradeStreamSubject
    from models.mark_list import MarkList
    from models.student import Student
    from models.year import Year


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
    code: Mapped[str] = mapped_column(String(20), nullable=False)

    # One-To-Many Relationships
    year: Mapped["Year"] = relationship(
        "Year",
        back_populates="subjects",
        repr=False,
        passive_deletes=True,
        init=False,
    )

    teacher_records: Mapped[List["TeacherRecord"]] = relationship(
        "TeacherRecord",
        back_populates="subject",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    # Many-To-Many Relationships
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
        """Return unique grades that have streams assigned to this subject."""
        seen = set()
        result = []
        for g in self._grades:
            if g is not None and g.id not in seen:
                seen.add(g.id)
                result.append(g)
        return sorted(result, key=sort_grade_key)

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
