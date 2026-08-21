#!/usr/bin/python3
"""Module for AcademicTerm class"""

import uuid
from datetime import date
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    UUID,
    CheckConstraint,
    Date,
    Enum,
    ForeignKeyConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin
from project.utils.enum import AcademicTermEnum

if TYPE_CHECKING:
    from project.models.assessment_scheme_component import AssessmentSchemeComponent
    from project.models.student_term_record import StudentTermRecord
    from project.models.year import Year


class AcademicTerm(SchoolScopedMixin, BaseModel):
    """docstring for AcademicTerm."""

    __tablename__ = "academic_terms"
    year_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False, index=True)
    name: Mapped[AcademicTermEnum] = mapped_column(
        Enum(
            AcademicTermEnum,
            name="academic_term_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
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

    assessment_scheme_components: Mapped[List["AssessmentSchemeComponent"]] = relationship(
        "AssessmentSchemeComponent",
        back_populates="academic_term",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="school,assessment_scheme_components",
    )

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_academic_term_id_school_id"),
        UniqueConstraint("year_id", "name", name="uq_academic_term_year_name"),
        ForeignKeyConstraint(
            ["year_id", "school_id"],
            ["years.id", "years.school_id"],
            name="fk_academic_terms_year_school",
            ondelete="CASCADE",
        ),
        CheckConstraint("start_date <= end_date", name="check_term_dates"),
        CheckConstraint(
            "registration_start <= registration_end",
            name="check_term_registration_dates",
        ),
    )
