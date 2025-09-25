#!/usr/bin/python3

import uuid
from dataclasses import dataclass

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from models.base.base_model import Base
from sqlalchemy import UUID


@dataclass
class StudentStreamLink(Base):
    __tablename__ = "student_stream_links"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("students.id", ondelete="CASCADE"),
        primary_key=True,
    )
    stream_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("streams.id", ondelete="CASCADE"),
        primary_key=True,
    )
