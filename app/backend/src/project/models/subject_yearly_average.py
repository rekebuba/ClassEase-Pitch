#!/usr/bin/python3
"""Module for yearly subject aggregates."""

import uuid
from typing import TYPE_CHECKING, Optional

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
    from project.models.student_year_record import StudentYearRecord
    from project.models.subject_offering import SubjectOffering


class SubjectYearlyAverage(SchoolScopedMixin, BaseModel):
    __tablename__ = "subject_yearly_averages"

    student_year_record_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    subject_offering_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    average: Mapped[Optional[float]] = mapped_column(Float, nullable=True, default=None)
    grade: Mapped[Optional[str]] = mapped_column(String(10), nullable=True, default=None)
    rank: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        default=None,
        comment="Rank of the student in this subject for this year.",
    )

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_subject_yearly_average_id_school_id"),
        UniqueConstraint(
            "student_year_record_id",
            "subject_offering_id",
            name="uq_subject_yearly_average_record_subject_pair",
        ),
        UniqueConstraint(
            "school_id",
            "student_year_record_id",
            "subject_offering_id",
            name="uq_subject_yearly_average_record_subject",
        ),
        ForeignKeyConstraint(
            ["student_year_record_id", "school_id"],
            ["student_year_records.id", "student_year_records.school_id"],
            name="fk_subject_yearly_average_year_record_school",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["subject_offering_id", "school_id"],
            ["subject_offerings.id", "subject_offerings.school_id"],
            name="fk_subject_yearly_average_subject_offering_school",
            ondelete="CASCADE",
        ),
    )

    student_year_record: Mapped["StudentYearRecord"] = relationship(
        "StudentYearRecord",
        back_populates="subject_yearly_averages",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="subject_yearly_averages",
    )
    subject_offering: Mapped["SubjectOffering"] = relationship(
        "SubjectOffering",
        back_populates="subject_yearly_averages",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="student_year_record,subject_yearly_averages",
    )
