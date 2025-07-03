#!/usr/bin/python3
"""Module for StudentTermRecord class"""

from typing import TYPE_CHECKING, List
from sqlalchemy import String, Integer, ForeignKey, Float
from models.assessment import Assessment
from models.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.section import Section
    from models.academic_term import AcademicTerm
    from models.student_year_record import StudentYearRecord
    from models.student import Student


class StudentTermRecord(BaseModel):
    """
    This model represents the average result of a student for a particular term and year.
    """

    __tablename__ = "student_term_records"
    student_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("students.id"), nullable=False
    )
    academic_term_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("academic_terms.id"), nullable=False
    )
    section_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("sections.id"), nullable=False
    )
    student_year_record_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("student_year_records.id"), nullable=True, default=None
    )
    average: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    rank: Mapped[int] = mapped_column(Integer, nullable=True, default=None)

    # Relationships
    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="student_term_records",
        init=False,
    )
    student_year_record: Mapped["StudentYearRecord"] = relationship(
        "StudentYearRecord",
        back_populates="student_term_records",
        init=False,
    )
    academic_term: Mapped["AcademicTerm"] = relationship(
        "AcademicTerm",
        back_populates="student_term_records",
        init=False,
    )
    section: Mapped["Section"] = relationship(
        "Section",
        back_populates="student_term_records",
        init=False,
    )
    assessments: Mapped[List["Assessment"]] = relationship(
        "Assessment",
        back_populates="student_term_record",
        default_factory=list,
        repr=False,
    )
