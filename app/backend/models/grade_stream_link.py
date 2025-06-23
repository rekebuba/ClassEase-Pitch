#!/usr/bin/python3
"""Module for Subject class"""

from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String
from models.base_model import Base


@dataclass
class GradeStreamLink(Base):
    __tablename__ = "grade_stream_links"

    grade_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("grades.id"), primary_key=True
    )
    stream_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("streams.id"), primary_key=True
    )
