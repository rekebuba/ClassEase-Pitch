#!/usr/bin/python3
"""Module for component-level assessment scores."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    UUID,
    DateTime,
    Float,
    ForeignKeyConstraint,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin

if TYPE_CHECKING:
    from project.models.assessment_scheme_component import AssessmentSchemeComponent
    from project.models.subject_term_result import SubjectTermResult
    from project.models.teacher_profile import TeacherProfile
    from project.models.teaching_assignment import TeachingAssignment


class Assessment(SchoolScopedMixin, BaseModel):
    """
    Component-level score entered for one subject term result.

    Authorization is anchored through teaching_assignment_id. Application services
    should only accept a score when the assignment points to the same subject
    offering and class section as the student's term result.
    """

    __tablename__ = "assessment_scores"

    subject_term_result_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    assessment_scheme_component_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    remarks: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    raw_score: Mapped[float] = mapped_column(Float, nullable=False)
    teaching_assignment_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(),
        nullable=True,
        default=None,
    )
    entered_by_teacher_profile_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(),
        nullable=True,
        default=None,
    )
    weighted_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        default=None,
    )
    entered_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_assessment_score_id_school_id"),
        UniqueConstraint(
            "school_id",
            "subject_term_result_id",
            "assessment_scheme_component_id",
            name="uq_assessment_score_result_component",
        ),
        ForeignKeyConstraint(
            ["subject_term_result_id", "school_id"],
            ["subject_term_results.id", "subject_term_results.school_id"],
            name="fk_assessment_score_subject_term_result_school",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["assessment_scheme_component_id", "school_id"],
            [
                "assessment_scheme_components.id",
                "assessment_scheme_components.school_id",
            ],
            name="fk_assessment_score_component_school",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["teaching_assignment_id", "school_id"],
            ["teaching_assignments.id", "teaching_assignments.school_id"],
            name="fk_assessment_score_teaching_assignment_school",
            ondelete="SET NULL",
        ),
        ForeignKeyConstraint(
            ["entered_by_teacher_profile_id", "school_id"],
            ["teacher_profiles.id", "teacher_profiles.school_id"],
            name="fk_assessment_score_entered_by_teacher_school",
            ondelete="SET NULL",
        ),
    )

    subject_term_result: Mapped["SubjectTermResult"] = relationship(
        "SubjectTermResult",
        back_populates="assessment_scores",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    assessment_scheme_component: Mapped["AssessmentSchemeComponent"] = relationship(
        "AssessmentSchemeComponent",
        back_populates="scores",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="subject_term_result",
    )
    teaching_assignment: Mapped[Optional["TeachingAssignment"]] = relationship(
        "TeachingAssignment",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="assessment_scheme_component,subject_term_result",
    )
    entered_by_teacher: Mapped[Optional["TeacherProfile"]] = relationship(
        "TeacherProfile",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="assessment_scheme_component,subject_term_result,teaching_assignment",
    )
