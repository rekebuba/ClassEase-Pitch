#!/usr/bin/python3
"""Module for StudentYearRecord class."""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    UUID,
    Float,
    ForeignKeyConstraint,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin

if TYPE_CHECKING:
    from project.models.class_section import ClassSection
    from project.models.grade import Grade
    from project.models.section import Section
    from project.models.stream import Stream
    from project.models.student import Student
    from project.models.student_enrollments import StudentEnrollment
    from project.models.student_term_record import StudentTermRecord
    from project.models.subject_yearly_average import SubjectYearlyAverage
    from project.models.year import Year


class StudentYearRecord(SchoolScopedMixin, BaseModel):
    """
    Canonical yearly academic record for one student enrollment.
    """

    __tablename__ = "student_year_records"

    student_enrollment_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    average: Mapped[Optional[float]] = mapped_column(Float, nullable=True, default=None)
    rank: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        default=None,
        comment="Overall rank of the student in the class for this year.",
    )
    promotion_status: Mapped[Optional[str]] = mapped_column(
        String(30),
        nullable=True,
        default=None,
    )

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_student_year_record_id_school_id"),
        UniqueConstraint(
            "school_id",
            "student_enrollment_id",
            name="uq_student_year_record_enrollment",
        ),
        ForeignKeyConstraint(
            ["student_enrollment_id", "school_id"],
            ["student_enrollments.id", "student_enrollments.school_id"],
            name="fk_student_year_record_enrollment_school",
            ondelete="CASCADE",
        ),
    )

    student_enrollment: Mapped["StudentEnrollment"] = relationship(
        "StudentEnrollment",
        back_populates="student_year_record",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    term_records: Mapped[List["StudentTermRecord"]] = relationship(
        "StudentTermRecord",
        back_populates="student_year_record",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="academic_term,student_enrollment,student_term_records",
    )
    subject_yearly_averages: Mapped[List["SubjectYearlyAverage"]] = relationship(
        "SubjectYearlyAverage",
        back_populates="student_year_record",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    student: AssociationProxy["Student"] = association_proxy(
        "student_enrollment",
        "student",
        default=None,
    )
    year: AssociationProxy["Year"] = association_proxy(
        "student_enrollment",
        "academic_year",
        default=None,
    )
    class_section: AssociationProxy["ClassSection"] = association_proxy(
        "student_enrollment",
        "class_section",
        default=None,
    )
    grade: AssociationProxy["Grade"] = association_proxy(
        "class_section",
        "grade",
        default=None,
    )
    section: AssociationProxy["Section"] = association_proxy(
        "class_section",
        "section",
        default=None,
    )
    stream: AssociationProxy[Optional["Stream"]] = association_proxy(
        "class_section",
        "stream",
        default=None,
    )
