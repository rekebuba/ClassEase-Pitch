#!/usr/bin/python3
"""Module for AssessmentSchemeComponent class"""

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
    from project.models.academic_term import AcademicTerm
    from project.models.assessment import Assessment
    from project.models.assessment_scheme import AssessmentScheme


class AssessmentSchemeComponent(SchoolScopedMixin, BaseModel):
    __tablename__ = "assessment_scheme_components"

    term_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    assessment_scheme_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    max_score: Mapped[float] = mapped_column(Float, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    academic_term: Mapped["AcademicTerm"] = relationship(
        "AcademicTerm",
        back_populates="assessment_scheme_components",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="school,assessment_scheme_components,components",
    )

    scheme: Mapped["AssessmentScheme"] = relationship(
        "AssessmentScheme",
        back_populates="components",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="school,academic_term,assessment_scheme_components",
    )
    scores: Mapped[List["Assessment"]] = relationship(
        "Assessment",
        back_populates="assessment_scheme_component",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="entered_by_teacher,subject_term_result,teaching_assignment",
    )

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_assessment_scheme_component_id_school_id"),
        UniqueConstraint(
            "school_id",
            "assessment_scheme_id",
            "name",
            name="uq_assessment_scheme_component_name",
        ),
        ForeignKeyConstraint(
            ["assessment_scheme_id", "school_id"],
            ["assessment_schemes.id", "assessment_schemes.school_id"],
            name="fk_assessment_scheme_component_scheme_school",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["term_id", "school_id"],
            ["academic_terms.id", "academic_terms.school_id"],
            name="fk_assessment_scheme_component_term_school",
            ondelete="CASCADE",
        ),
    )
