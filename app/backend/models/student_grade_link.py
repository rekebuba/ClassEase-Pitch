#!/usr/bin/python3

from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column
from sqlmodel import ForeignKey
from models.base.base_model import Base
from models.base.column_type import UUIDType
import uuid


@dataclass
class StudentGradeLink(Base):
    __tablename__ = "student_grade_links"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("students.id"),
        primary_key=True,
    )
    grade_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("grades.id"),
        primary_key=True,
    )
