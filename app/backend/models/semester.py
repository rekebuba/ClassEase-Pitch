#!/usr/bin/python3
"""Module for Semester class"""

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel


class Semester(BaseModel):
    """docstring for Semester."""

    __tablename__ = "semesters"
    event_id: Mapped[str] = mapped_column(
        String(225), ForeignKey("events.id"), nullable=False
    )
    name: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    semester_records = relationship(
        "STUDSemesterRecord", back_populates="semesters", uselist=False
    )
