#!/usr/bin/python3

from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column
from sqlmodel import ForeignKey
from models.base.base_model import Base
from models.base.column_type import UUIDType
import uuid


@dataclass
class SubjectStreamLink(Base):
    """SubjectStreamLink Model"""

    __tablename__ = "subject_stream_links"

    subject_id: Mapped[uuid.UUID] = mapped_column(
        "subject_id",
        UUIDType(),
        ForeignKey("subjects.id"),
        primary_key=True,
    )
    stream_id: Mapped[uuid.UUID] = mapped_column(
        "stream_id",
        UUIDType(),
        ForeignKey("streams.id"),
        primary_key=True,
    )
