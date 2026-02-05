#!/usr/bin/python3
"""Module for MarkList class"""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, Enum, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.student_term_record import StudentTermRecord
from project.utils.enum import MarkListTypeEnum

if TYPE_CHECKING:
    from project.models.student import Student
    from project.models.subject import Subject


class MarkList(BaseModel):
    """
    This model represents a list of marks for students in various assessments.
    It includes details about the student, grade, section, subject, teacher's record,
    semester, year, type of assessment, percentage contribution to the final score,
     and the actual score obtained.
    """

    __tablename__ = "mark_lists"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    student_term_record_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("student_term_records.id", ondelete="CASCADE"),
        nullable=False,
    )
    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
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
    score: Mapped[float] = mapped_column(Float, nullable=True, default=None)

    # Relationships
    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="mark_lists",
        repr=False,
        passive_deletes=True,
        init=False,
    )
    student_term_record: Mapped["StudentTermRecord"] = relationship(
        "StudentTermRecord",
        back_populates="mark_lists",
        repr=False,
        passive_deletes=True,
        init=False,
    )
    subject: Mapped["Subject"] = relationship(
        "Subject",
        back_populates="mark_lists",
        repr=False,
        passive_deletes=True,
        init=False,
    )
