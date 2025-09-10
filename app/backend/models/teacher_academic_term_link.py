#!/usr/bin/python3
"""Module for TeacherAcademicTermLink class"""

import uuid
from dataclasses import dataclass

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base.base_model import Base
from models.base.column_type import UUIDType


@dataclass
class TeacherAcademicTermLink(Base):
    """
    This model represents the record of teachers, including their associated subjects, grades, and sections.
    """

    __tablename__ = "teacher_academic_term_links"

    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("teachers.id", ondelete="CASCADE"),
        primary_key=True,
    )
    academic_term_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("academic_terms.id", ondelete="CASCADE"),
        primary_key=True,
    )
