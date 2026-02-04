#!/usr/bin/python3
"""Module for Section class"""

import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel

if TYPE_CHECKING:
    from project.models.grade import Grade
    from project.models.student import Student
    from project.models.student_term_record import StudentTermRecord
    from project.models.subject import Subject
    from project.models.teacher_record import TeacherRecord


class Section(BaseModel):
    """
    Represents a section within a grade.
    """

    __tablename__ = "sections"
    grade_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
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
        secondary="teacher_record_links",
        back_populates="sections",
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

    _teacher_subjects: AssociationProxy[List["Subject"]] = association_proxy(
        "teacher_records",
        "subject",
        default_factory=list,
    )

    @property
    def teacher_subjects(self) -> List["Subject"]:
        """Return unique, non-null teacher_subjects."""
        seen = set()
        result = []
        for s in self._teacher_subjects:
            if s is not None and s.id not in seen:
                seen.add(s.id)
                result.append(s)

        return sorted(result, key=lambda x: x.name)
