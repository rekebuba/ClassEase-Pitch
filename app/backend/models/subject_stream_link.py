#!/usr/bin/python3

from dataclasses import dataclass
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlmodel import ForeignKey
from models.base_model import Base


@dataclass
class SubjectStreamLink(Base):
    """SubjectStreamLink Model"""

    __tablename__ = "subject_stream_links"

    subject_id: Mapped[str] = mapped_column(
        "subject_id",
        String(36),
        ForeignKey("subjects.id"),
        primary_key=True,
    )
    stream_id: Mapped[str] = mapped_column(
        "stream_id",
        String(36),
        ForeignKey("streams.id"),
        primary_key=True,
    )
