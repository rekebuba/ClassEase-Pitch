#!/usr/bin/python3

from dataclasses import dataclass
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlmodel import ForeignKey
from models.base_model import Base


@dataclass
class SubjectGradeLink(Base):
    """SubjectGradeLink Model"""

    __tablename__ = "subject_grade_links"

    subject_id: Mapped[str] = mapped_column(
        "subject_id",
        String(36),
        ForeignKey("subjects.id"),
        primary_key=True,
    )
    grade_id: Mapped[str] = mapped_column(
        "grade_id",
        String(36),
        ForeignKey("grades.id"),
        primary_key=True,
    )
