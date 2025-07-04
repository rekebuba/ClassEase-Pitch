#!/usr/bin/python3
"""Module for TeachersRecord class"""

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel


class TeachersRecord(BaseModel):
    """
    This model represents the record of teachers, including their associated subjects, grades, and sections.
    """

    __tablename__ = "teachers_records"
    teacher_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("teachers.id"), nullable=False
    )
    academic_term_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("academic_terms.id"), nullable=False
    )
    yearly_subject_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("yearly_subjects.id"), nullable=False
    )
    section_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("sections.id"), nullable=True, default=None
    )

    mark_list = relationship(
        "MarkList",
        backref="teachers_record",
        cascade="save-update",
        passive_deletes=True,
    )
    assessment = relationship(
        "Assessment",
        backref="teachers_record",
        cascade="save-update",
        passive_deletes=True,
    )
