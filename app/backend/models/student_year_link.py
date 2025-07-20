#!/usr/bin/python3

from dataclasses import dataclass
from sqlalchemy import Float, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlmodel import ForeignKey
from models.base.base_model import Base
from models.base.column_type import UUIDType
import uuid


@dataclass
class StudentYearLink(Base):
    __tablename__ = "student_year_links"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("students.id"),
        primary_key=True,
    )
    year_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("years.id"),
        primary_key=True,
    )

    average: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    rank: Mapped[int] = mapped_column(Integer, nullable=True, default=None)
