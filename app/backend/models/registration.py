#!/usr/bin/python3
"""Module for Section class"""

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from models.base_model import BaseModel


class Registration(BaseModel):
    """docstring for Registration."""

    __tablename__ = "registrations"
    student_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("students.id"), nullable=False
    )
    subject_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("subjects.id"), nullable=False
    )
    semester_id: Mapped[str] = mapped_column(
        String(120), ForeignKey("semesters.id"), nullable=False
    )
    registration_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
