#!/usr/bin/python3

import uuid
from dataclasses import dataclass

from sqlalchemy import Float, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from models.base.base_model import Base
from sqlalchemy import UUID


@dataclass
class StudentYearLink(Base):
    __tablename__ = "student_year_links"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("students.id", ondelete="CASCADE"),
        primary_key=True,
    )
    year_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("years.id", ondelete="CASCADE"),
        primary_key=True,
    )

    average: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    rank: Mapped[int] = mapped_column(Integer, nullable=True, default=None)
