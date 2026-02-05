#!/usr/bin/python3

import uuid
from dataclasses import dataclass

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from project.models.base.base_model import Base


@dataclass
class StudentSectionLink(Base):
    __tablename__ = "student_section_links"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("students.id", ondelete="CASCADE"),
        primary_key=True,
    )
    section_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("sections.id", ondelete="CASCADE"),
        primary_key=True,
    )
