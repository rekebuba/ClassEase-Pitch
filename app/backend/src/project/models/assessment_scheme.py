#!/usr/bin/python3
"""Module for AssessmentScheme class"""

from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin

if TYPE_CHECKING:
    from project.models.assessment_scheme_component import AssessmentSchemeComponent
    from project.models.subject_offering import SubjectOffering


class AssessmentScheme(SchoolScopedMixin, BaseModel):
    __tablename__ = "assessment_schemes"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    components: Mapped[List["AssessmentSchemeComponent"]] = relationship(
        "AssessmentSchemeComponent",
        back_populates="scheme",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="assessment_scheme_components",
    )
    subject_offerings: Mapped[List["SubjectOffering"]] = relationship(
        "SubjectOffering",
        back_populates="assessment_scheme",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="grade_stream,subject_offerings",
    )

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_assessment_scheme_id_school_id"),
        UniqueConstraint("school_id", "name", name="uq_assessment_scheme_school_name"),
    )
