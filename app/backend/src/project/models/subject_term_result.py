#!/usr/bin/python3
"""Subject-level term result model."""

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
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin

if TYPE_CHECKING:
    from project.models.assessment import Assessment
    from project.models.student_term_record import StudentTermRecord
    from project.models.subject_offering import SubjectOffering
    from project.models.teaching_assignment import TeachingAssignment


class SubjectTermResult(SchoolScopedMixin, BaseModel):
    """
    Aggregate result for one student, one term, and one subject offering.

    Component-level entries live in Assessment. This row stores the calculated
    total, grade, and optional rank used on report cards.
    """

    __tablename__ = "subject_term_results"

    teaching_assignment_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(), nullable=False)
    student_term_record_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    subject_offering_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    total: Mapped[Optional[float]] = mapped_column(Float, nullable=True, default=None)
    grade: Mapped[Optional[str]] = mapped_column(
        String(10),
        nullable=True,
        default=None,
    )
    rank: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        default=None,
        comment="Rank of the student in this subject for this term.",
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
        UniqueConstraint("id", "school_id", name="uq_subject_term_result_id_school_id"),
        UniqueConstraint(
            "school_id",
            "student_term_record_id",
            "subject_offering_id",
            name="uq_subject_term_result_term_subject",
        ),
        ForeignKeyConstraint(
            ["teaching_assignment_id", "school_id"],
            ["teaching_assignments.id", "teaching_assignments.school_id"],
            name="fk_subject_term_result_teaching_assignment_school",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["student_term_record_id", "school_id"],
            ["student_term_records.id", "student_term_records.school_id"],
            name="fk_subject_term_result_student_term_record_school",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["subject_offering_id", "school_id"],
            ["subject_offerings.id", "subject_offerings.school_id"],
            name="fk_subject_term_result_subject_offering_school",
            ondelete="CASCADE",
        ),
    )

    teaching_assignment: Mapped[Optional["TeachingAssignment"]] = relationship(
        "TeachingAssignment",
        back_populates="subject_term_results",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="subject_results,subject_term_results",
    )
    student_term_record: Mapped["StudentTermRecord"] = relationship(
        "StudentTermRecord",
        back_populates="subject_results",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="subject_term_results,teaching_assignment",
    )
    subject_offering: Mapped["SubjectOffering"] = relationship(
        "SubjectOffering",
        back_populates="subject_term_results",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="student_term_record,subject_results,teaching_assignment",
    )
    assessment_scores: Mapped[List["Assessment"]] = relationship(
        "Assessment",
        back_populates="subject_term_result",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="assessment_scheme_component,entered_by_teacher,scores,teaching_assignment",
    )
