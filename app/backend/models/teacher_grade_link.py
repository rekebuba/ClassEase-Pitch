#!/usr/bin/python3
"""Module for Teacher class"""

from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from models.base.base_model import Base
from models.base.column_type import UUIDType
import uuid


@dataclass
class TeacherGradeLink(Base):
    __tablename__ = "teacher_grade_links"

    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("teachers.id"), primary_key=True
    )
    grade_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("grades.id"), primary_key=True
    )
