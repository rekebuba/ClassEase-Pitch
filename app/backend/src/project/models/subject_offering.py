#!/usr/bin/python3
"""Module for SubjectOffering class"""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import UUID, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin

if TYPE_CHECKING:
    from project.models.assessment_scheme import AssessmentScheme
    from project.models.grade_stream import GradeStream
    from project.models.school import School
    from project.models.subject import Subject
    from project.models.subject_term_result import SubjectTermResult
    from project.models.subject_yearly_average import SubjectYearlyAverage
    from project.models.teaching_assignment import TeachingAssignment
    from project.models.year import Year


class SubjectOffering(SchoolScopedMixin, BaseModel):
    __tablename__ = "subject_offerings"

    assessment_scheme_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    year_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    subject_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    grade_stream_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)

    # Relationships
    year: Mapped["Year"] = relationship(
        "Year",
        back_populates="subject_offerings",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="subject_offerings",
    )
    subject: Mapped["Subject"] = relationship(
        "Subject",
        back_populates="subject_offerings",
        init=False,
        repr=False,
        overlaps="year,subject_offerings",
    )
    grade_stream: Mapped["GradeStream"] = relationship(
        "GradeStream",
        back_populates="subject_offerings",
        init=False,
        repr=False,
        overlaps="grade,subject,year,subject_offerings",
    )

    teaching_assignments: Mapped[List["TeachingAssignment"]] = relationship(
        "TeachingAssignment",
        back_populates="subject_offering",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="teaching_assignments",
    )
    subject_yearly_averages: Mapped[List["SubjectYearlyAverage"]] = relationship(
        "SubjectYearlyAverage",
        back_populates="subject_offering",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="subject_yearly_averages",
    )
    assessment_scheme: Mapped[Optional["AssessmentScheme"]] = relationship(
        "AssessmentScheme",
        back_populates="subject_offerings",
        init=False,
        repr=False,
        overlaps="grade_stream,school,subject,subject_offerings,year",
    )
    subject_term_results: Mapped[List["SubjectTermResult"]] = relationship(
        "SubjectTermResult",
        back_populates="subject_offering",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="subject_offering,subject_results",
    )
    school: Mapped["School"] = relationship(
        "School",
        back_populates="subject_offerings",
        init=False,
        repr=False,
        overlaps="assessment_scheme,grade_stream,subject,subject_offerings,year",
    )

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_subject_offering_id_school_id"),
        UniqueConstraint(
            "school_id",
            "year_id",
            "grade_stream_id",
            "subject_id",
            name="uq_subject_offering_scope",
        ),
        ForeignKeyConstraint(
            ["year_id", "school_id"],
            ["years.id", "years.school_id"],
            name="fk_subject_offerings_year_school",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["subject_id", "school_id"],
            ["subjects.id", "subjects.school_id"],
            name="fk_subject_offerings_subject_definition_school",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["grade_stream_id", "school_id"],
            ["grade_streams.id", "grade_streams.school_id"],
            name="fk_subject_offerings_grade_stream_school",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["assessment_scheme_id", "school_id"],
            ["assessment_schemes.id", "assessment_schemes.school_id"],
            name="fk_subject_offerings_assessment_scheme_school",
            ondelete="SET NULL",
        ),
    )
