#!/usr/bin/python3
"""Module for Subject class"""

from typing import TYPE_CHECKING, List

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin

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
    grade_streams = association_proxy(
        "subject_offerings",
        "grade_stream",
    )
