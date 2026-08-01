#!/usr/bin/python3
"""Module for Subject class"""

from typing import TYPE_CHECKING, List

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin
from project.models.grade import Grade
from project.models.stream import Stream
from project.utils.utils import sort_grade_key

if TYPE_CHECKING:
    from project.models.subject_offering import SubjectOffering
    from project.models.teacher_subject import TeacherSubject


class Subject(SchoolScopedMixin, BaseModel):
    """
    Master subject definition owned by a school.

    Year, grade, and stream-specific availability is modeled by SubjectOffering.
    """

    __tablename__ = "subjects"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)

    __table_args__ = (
        UniqueConstraint("school_id", "code", name="uq_subject_definition_school_code"),
        UniqueConstraint("school_id", "name", name="uq_subject_definition_school_name"),
        UniqueConstraint("id", "school_id", name="uq_subject_id_school_id"),
    )

    # Many-To-Many Relationships
    teacher_subjects: Mapped[List["TeacherSubject"]] = relationship(
        "TeacherSubject",
        back_populates="subject",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="teacher_subjects",
    )
    subject_offerings: Mapped[List["SubjectOffering"]] = relationship(
        "SubjectOffering",
        back_populates="subject",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="subject_offerings",
    )

    # Association proxy
    _grades: AssociationProxy[List["Grade"]] = association_proxy(
        "subject_offerings",
        "grade",
        default_factory=list,
    )
    _streams: AssociationProxy[List["Stream"]] = association_proxy(
        "subject_offerings",
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
