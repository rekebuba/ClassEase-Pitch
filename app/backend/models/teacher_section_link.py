#!/usr/bin/python3

import uuid
from dataclasses import dataclass

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from models.base.base_model import Base
from models.base.column_type import UUIDType


@dataclass
class TeacherSectionLink(Base):
    __tablename__ = "teacher_section_links"

    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("teachers.id", ondelete="CASCADE"),
        primary_key=True,
    )
    section_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("sections.id", ondelete="CASCADE"),
        primary_key=True,
    )
