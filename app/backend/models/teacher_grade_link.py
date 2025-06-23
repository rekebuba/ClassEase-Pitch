#!/usr/bin/python3
"""Module for Teacher class"""

from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String
from models.base_model import Base


@dataclass
class TeacherGradeLink(Base):
    __tablename__ = "teacher_grade_links"

    teacher_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("teachers.id"), primary_key=True
    )
    grade_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("grades.id"), primary_key=True
    )
