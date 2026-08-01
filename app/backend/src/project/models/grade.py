#!/usr/bin/python3
"""Module for Grade class"""

from typing import TYPE_CHECKING, List

from sqlalchemy import Enum, UniqueConstraint
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin
from project.utils.enum import GradeEnum, GradeLevelEnum

if TYPE_CHECKING:
    from project.models.section import Section
    from project.models.stream import Stream
    from project.models.subject import Subject
    from project.models.subject_offering import SubjectOffering


class Grade(SchoolScopedMixin, BaseModel):
    """Grade Model"""

    __tablename__ = "grades"

    # Database column
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

    __table_args__ = (UniqueConstraint("id", "school_id", name="uq_grade_id_school_id"),)

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
    subject_offerings: Mapped[List["SubjectOffering"]] = relationship(
        "SubjectOffering",
        back_populates="grade",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="subject_offerings",
    )

    # Association proxy
    _subjects: AssociationProxy[List["Subject"]] = association_proxy(
        "subject_offerings",
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
