#!/usr/bin/python3
"""Module for Section class"""

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from models.base.base_model import BaseModel
from models.base.column_type import UUIDType
import uuid


class Registration(BaseModel):
    """docstring for Registration."""

    __tablename__ = "registrations"
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("students.id", ondelete='CASCADE'), nullable=False
    )
    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("subjects.id", ondelete='CASCADE'), nullable=False
    )
    semester_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("semesters.id", ondelete='CASCADE'), nullable=False
    )
    registration_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
