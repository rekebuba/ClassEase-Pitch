#!/usr/bin/python3
"""Module for Subject class"""

import uuid
from dataclasses import dataclass

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base.base_model import Base
from sqlalchemy import UUID


@dataclass
class GradeStreamLink(Base):
    __tablename__ = "grade_stream_links"

    grade_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("grades.id", ondelete="CASCADE"),
        primary_key=True,
    )
    stream_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("streams.id", ondelete="CASCADE"),
        primary_key=True,
    )
