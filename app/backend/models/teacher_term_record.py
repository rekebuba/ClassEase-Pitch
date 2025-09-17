#!/usr/bin/python3
"""Module for TeacherTermRecord class"""

import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base.base_model import BaseModel
from models.base.column_type import UUIDType


class TeacherTermRecord(BaseModel):
    __tablename__ = "teacher_term_records"
    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False
    )
    academic_term_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("academic_terms.id", ondelete="CASCADE"), nullable=False
    )
    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )
    grade_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("grades.id", ondelete="CASCADE"), nullable=False
    )
    section_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("sections.id", ondelete="CASCADE"), nullable=False
    )
    stream_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("streams.id", ondelete="CASCADE"),
        nullable=True,
        default=None,
    )

    # One-To-Many Relationships
