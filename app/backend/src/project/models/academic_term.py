#!/usr/bin/python3
"""Module for AcademicTerm class"""

import uuid
from datetime import date
from typing import TYPE_CHECKING, List, Optional

import sqlalchemy as sa
from sqlalchemy import UUID, Date, Enum, ForeignKey
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.grade import Grade
from project.models.subject import Subject
from project.utils.enum import AcademicTermEnum
from project.utils.utils import sort_grade_key

if TYPE_CHECKING:
    from project.models.student import Student
    from project.models.student_term_record import StudentTermRecord
    from project.models.teacher_record import TeacherRecord
    from project.models.year import Year


class AcademicTerm(BaseModel):
    """docstring for AcademicTerm."""

    __tablename__ = "academic_terms"
    year_id: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("years.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[AcademicTermEnum] = mapped_column(
        Enum(
            AcademicTermEnum,
            name="academic_term_enum",
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
    )

    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    registration_start: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    registration_end: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Relationships
    year: Mapped["Year"] = relationship(
        "Year",
        back_populates="academic_terms",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    student_term_records: Mapped[List["StudentTermRecord"]] = relationship(
        "StudentTermRecord",
        back_populates="academic_term",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    students: Mapped[List["Student"]] = relationship(
        "Student",
        secondary="student_academic_term_links",
        back_populates="academic_terms",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    # One-To-Many Relationships
    teacher_records: Mapped[List["TeacherRecord"]] = relationship(
        "TeacherRecord",
        back_populates="academic_term",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    _grades: AssociationProxy[List["Grade"]] = association_proxy(
        "teacher_records",
        "grade",
        default_factory=list,
    )

    _subjects: AssociationProxy[List["Subject"]] = association_proxy(
        "teacher_records",
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

    __table_args__ = (
        sa.CheckConstraint("start_date <= end_date", name="check_term_dates"),
        sa.CheckConstraint(
            "registration_start <= registration_end",
            name="check_term_registration_dates",
        ),
    )
