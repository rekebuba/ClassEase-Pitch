#!/usr/bin/python3

import uuid
from dataclasses import dataclass

from sqlalchemy import UUID, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from project.models.base.base_model import Base


@dataclass
class StudentAcademicTermLink(Base):
    __tablename__ = "student_academic_term_links"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("students.id", ondelete="CASCADE"),
        primary_key=True,
    )
    academic_term_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("academic_terms.id", ondelete="CASCADE"),
        primary_key=True,
    )

    average: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    rank: Mapped[int] = mapped_column(Integer, nullable=True, default=None)
