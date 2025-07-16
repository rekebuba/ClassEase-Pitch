#!/usr/bin/python3
"""Module for TeachersRecord class"""

from typing import TYPE_CHECKING, List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base.base_model import BaseModel

from models.base.column_type import UUIDType
import uuid
if TYPE_CHECKING:
    from models.teacher import Teacher
    from models.academic_term import AcademicTerm
    from models.yearly_subject import YearlySubject
    from models.section import Section


class TeachersRecord(BaseModel):
    """
    This model represents the record of teachers, including their associated subjects, grades, and sections.
    """

    __tablename__ = "teacher_records"
    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("teachers.id"), nullable=False
    )
    academic_term_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("academic_terms.id"), nullable=False
    )

    teacher: Mapped["Teacher"] = relationship(
        "Teacher",
        back_populates="teacher_records",
        init=False,
        repr=False,
    )
    academic_term: Mapped["AcademicTerm"] = relationship(
        "AcademicTerm",
        back_populates="teacher_records",
        init=False,
    )

    # Many-to-many relationships
    yearly_subjects_link: Mapped[List["YearlySubject"]] = relationship(
        "YearlySubject",
        back_populates="teacher_records_link",
        secondary="teacher_yearly_subject_links",
        default_factory=list,
        repr=False,
    )
    sections_link: Mapped[List["Section"]] = relationship(
        "Section",
        back_populates="teacher_records_link",
        secondary="teacher_record_section_links",
        default_factory=list,
        repr=False,
    )
