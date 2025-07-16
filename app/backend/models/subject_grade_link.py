#!/usr/bin/python3

from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column
from sqlmodel import ForeignKey
from models.base.base_model import Base
from models.base.column_type import UUIDType
import uuid


@dataclass
class SubjectGradeLink(Base):
    """SubjectGradeLink Model"""

    __tablename__ = "subject_grade_links"

    subject_id: Mapped[uuid.UUID] = mapped_column(
        "subject_id",
        UUIDType(),
        ForeignKey("subjects.id"),
        primary_key=True,
    )
    grade_id: Mapped[uuid.UUID] = mapped_column(
        "grade_id",
        UUIDType(),
        ForeignKey("grades.id"),
        primary_key=True,
    )
