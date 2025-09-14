#!/usr/bin/python3

import uuid
from dataclasses import dataclass

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from models.base.base_model import Base
from models.base.column_type import UUIDType


@dataclass
class GradeSectionLink(Base):
    __tablename__ = "grade_section_links"

    section_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("sections.id", ondelete="CASCADE"),
        primary_key=True,
    )
    grade_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("grades.id", ondelete="CASCADE"),
        primary_key=True,
    )
