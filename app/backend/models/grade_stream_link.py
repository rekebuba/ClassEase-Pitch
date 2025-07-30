#!/usr/bin/python3
"""Module for Subject class"""

from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from models.base.base_model import Base
from models.base.column_type import UUIDType
import uuid


@dataclass
class GradeStreamLink(Base):
    __tablename__ = "grade_stream_links"

    grade_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("grades.id", ondelete='CASCADE'),
        primary_key=True,
    )
    stream_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("streams.id", ondelete='CASCADE'),
        primary_key=True,
    )
