#!/usr/bin/python3
"""Module for AcademicTerm class"""

import uuid
from datetime import date
from typing import TYPE_CHECKING, List, Optional

import sqlalchemy as sa
from sqlalchemy import Date, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base.base_model import BaseModel
from models.base.column_type import UUIDType
from utils.enum import AcademicTermEnum

if TYPE_CHECKING:
    from models.student import Student
    from models.student_term_record import StudentTermRecord
    from models.teacher_record import TeacherRecord
    from models.year import Year


class AcademicTerm(BaseModel):
    """docstring for AcademicTerm."""

    __tablename__ = "academic_terms"
    year_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("years.id", ondelete="CASCADE"), nullable=False
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

    __table_args__ = (
        sa.CheckConstraint("start_date <= end_date", name="check_term_dates"),
        sa.CheckConstraint(
            "registration_start <= registration_end",
            name="check_term_registration_dates",
        ),
    )
