#!/usr/bin/python3
"""Module for StudentTermRecord class."""

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
    from project.models.academic_term import AcademicTerm
    from project.models.class_section import ClassSection
    from project.models.grade import Grade
    from project.models.section import Section
    from project.models.stream import Stream
    from project.models.student import Student
    from project.models.student_enrollments import StudentEnrollment
    from project.models.student_year_record import StudentYearRecord
    from project.models.subject_term_result import SubjectTermResult


class StudentTermRecord(SchoolScopedMixin, BaseModel):
    """
    Report-card header for one student enrollment in one academic term.

    Subject rows are represented by SubjectTermResult. This record stores the
    aggregate term outcome such as overall average, overall rank, and status.
    """

    __tablename__ = "student_term_records"

    student_enrollment_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    academic_term_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    student_year_record_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(),
        nullable=True,
        default=None,
    )
    average: Mapped[Optional[float]] = mapped_column(Float, nullable=True, default=None)
    rank: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        default=None,
        comment="Overall rank of the student in the class for this term.",
    )
    pass_status: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        default=None,
    )
    teacher_remarks: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        default=None,
    )

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_student_term_record_id_school_id"),
        UniqueConstraint(
            "school_id",
            "student_enrollment_id",
            "academic_term_id",
            name="uq_student_term_record_enrollment_term",
        ),
        ForeignKeyConstraint(
            ["student_enrollment_id", "school_id"],
            ["student_enrollments.id", "student_enrollments.school_id"],
            name="fk_student_term_record_enrollment_school",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["student_year_record_id", "school_id"],
            ["student_year_records.id", "student_year_records.school_id"],
            name="fk_student_term_record_year_record_school",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["academic_term_id", "school_id"],
            ["academic_terms.id", "academic_terms.school_id"],
            name="fk_student_term_record_academic_term_school",
            ondelete="CASCADE",
        ),
    )

    student_enrollment: Mapped["StudentEnrollment"] = relationship(
        "StudentEnrollment",
        back_populates="term_records",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="student_term_records",
    )
    student_year_record: Mapped[Optional["StudentYearRecord"]] = relationship(
        "StudentYearRecord",
        back_populates="term_records",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="student_enrollment,student_term_records,term_records",
    )
    academic_term: Mapped["AcademicTerm"] = relationship(
        "AcademicTerm",
        back_populates="student_term_records",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="student_enrollment,student_year_record,term_records",
    )
    subject_results: Mapped[List["SubjectTermResult"]] = relationship(
        "SubjectTermResult",
        back_populates="student_term_record",
        default_factory=list,
        init=False,
        repr=False,
        passive_deletes=True,
    )

    student: AssociationProxy["Student"] = association_proxy(
        "student_enrollment",
        "student",
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
