#!/usr/bin/python3

import uuid
from dataclasses import dataclass

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from project.models.base.base_model import Base
from sqlalchemy import UUID


@dataclass
class GradeSectionLink(Base):
    __tablename__ = "grade_section_links"

    section_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("sections.id", ondelete="CASCADE"),
        primary_key=True,
    )
    grade_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("grades.id", ondelete="CASCADE"),
        primary_key=True,
    )
