#!/usr/bin/python3
"""Module for Grade class"""

import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import UUID, Enum, ForeignKey
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.utils.enum import GradeEnum, GradeLevelEnum

if TYPE_CHECKING:
    from project.models.grade_stream_subject import GradeStreamSubject
    from project.models.section import Section
    from project.models.stream import Stream
    from project.models.student import Student
    from project.models.student_term_record import StudentTermRecord
    from project.models.subject import Subject
    from project.models.year import Year


class Grade(BaseModel):
    """Grade Model"""

    __tablename__ = "grades"

    # Database column
    year_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("years.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    grade: Mapped[GradeEnum] = mapped_column(
        Enum(
            GradeEnum,
            name="grade_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )
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

    # Many-To-One Relationships
    year: Mapped["Year"] = relationship(
        "Year",
        back_populates="grades",
        repr=False,
        passive_deletes=True,
        init=False,
    )

    # One-To-Many Relationships
    sections: Mapped[List["Section"]] = relationship(
        "Section",
        back_populates="grade",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    streams: Mapped[List["Stream"]] = relationship(
        "Stream",
        back_populates="grade",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    students: Mapped[List["Student"]] = relationship(
        "Student",
        back_populates="grade",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    student_term_records: Mapped[List["StudentTermRecord"]] = relationship(
        "StudentTermRecord",
        back_populates="grade",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    # Association Object
    grade_stream_subjects: Mapped[List["GradeStreamSubject"]] = relationship(
        "GradeStreamSubject",
        back_populates="grade",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    # Association proxy
    _subjects: AssociationProxy[List["Subject"]] = association_proxy(
        "grade_stream_subjects",
        "subject",
        default_factory=list,
    )

    @property
    def subjects(self) -> List["Subject"]:
        """Return unique, non-null subjects."""
        seen = set()
        result = []
        for s in self._subjects:
            if s is not None and s.id not in seen:
                seen.add(s.id)
                result.append(s)

        return sorted(result, key=lambda x: x.name)
