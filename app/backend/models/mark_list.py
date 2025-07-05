#!/usr/bin/python3
"""Module for MarkList class"""

from sqlalchemy import Enum, String, Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column
from extension.enums.enum import MarkListTypeEnum
from models.base_model import BaseModel


class MarkList(BaseModel):
    """
    This model represents a list of marks for students in various assessments. It includes details about the student, grade, section, subject, teacher's record, semester, year, type of assessment, percentage contribution to the final score, and the actual score obtained.
    """

    __tablename__ = "mark_lists"

    student_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("students.id"), nullable=False
    )
    student_term_record_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("student_term_records.id"), nullable=False
    )
    yearly_subject_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("yearly_subjects.id"), nullable=False
    )
    type: Mapped[MarkListTypeEnum] = mapped_column(
        Enum(
            MarkListTypeEnum,
            name="mark_list_type",
            value_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )
    percentage: Mapped[int] = mapped_column(Integer, nullable=False)
    score = mapped_column(Float, nullable=True, default=None)
