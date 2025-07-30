#!/usr/bin/python3

from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column
from sqlmodel import ForeignKey
from models.base.base_model import Base
from models.base.column_type import UUIDType
import uuid


@dataclass
class StudentSectionLink(Base):
    __tablename__ = "student_section_links"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("students.id", ondelete='CASCADE'),
        primary_key=True,
    )
    section_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("sections.id", ondelete='CASCADE'),
        primary_key=True,
    )
