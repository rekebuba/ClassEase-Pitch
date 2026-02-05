#!/usr/bin/python3
"""Module for Section class"""

import uuid

from sqlalchemy import UUID, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from project.models.base.base_model import BaseModel


class Registration(BaseModel):
    """docstring for Registration."""

    __tablename__ = "registrations"
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )
    registration_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
