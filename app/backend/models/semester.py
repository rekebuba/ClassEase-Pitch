#!/usr/bin/python3
"""Module for Semester class"""

from typing import TYPE_CHECKING, List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel

if TYPE_CHECKING:
    from models.stud_semester_record import STUDSemesterRecord


class Semester(BaseModel):
    """docstring for Semester."""

    __tablename__ = "semesters"
    event_id: Mapped[str] = mapped_column(
        String(225), ForeignKey("events.id"), nullable=False
    )
    name: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    semester_records: Mapped[List["STUDSemesterRecord"]] = relationship(
        "STUDSemesterRecord",
        back_populates="semesters",
        uselist=False,
        init=False,
    )
