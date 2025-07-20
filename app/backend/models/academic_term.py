#!/usr/bin/python3
"""Module for AcademicTerm class"""

from datetime import date
from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extension.enums.enum import AcademicTermEnum
from models.base.base_model import BaseModel
import sqlalchemy as sa

from models.base.column_type import UUIDType
import uuid


if TYPE_CHECKING:
    from models.student_term_record import StudentTermRecord
    from models.year import Year
    from models.teacher_record import TeachersRecord
    from models.student import Student


class AcademicTerm(BaseModel):
    """docstring for AcademicTerm."""

    __tablename__ = "academic_terms"
    year_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("years.id"), nullable=False
    )
    name: Mapped[AcademicTermEnum] = mapped_column(
        Enum(
            AcademicTermEnum,
            name="academic_term_enum",
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
    )

    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    registration_start: Mapped[date] = mapped_column(Date, nullable=True)
    registration_end: Mapped[date] = mapped_column(Date, nullable=True)

    # Relationships
    year: Mapped["Year"] = relationship(
        "Year",
        back_populates="academic_terms",
        init=False,
    )
    student_term_records: Mapped[List["StudentTermRecord"]] = relationship(
        "StudentTermRecord",
        back_populates="academic_term",
        default_factory=list,
        repr=False,
    )
    teacher_records: Mapped[List["TeachersRecord"]] = relationship(
        "TeachersRecord",
        back_populates="academic_term",
        default_factory=list,
        repr=False,
    )

    student_links: Mapped[List["Student"]] = relationship(
        "Student",
        secondary="student_academic_term_links",
        back_populates="academic_term_links",
        default_factory=list,
        repr=False,
    )

    __table_args__ = (
        sa.CheckConstraint("start_date <= end_date", name="check_term_dates"),
        sa.CheckConstraint(
            "registration_start <= registration_end",
            name="check_term_registration_dates",
        ),
    )
