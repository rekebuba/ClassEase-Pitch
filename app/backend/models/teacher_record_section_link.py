#!/usr/bin/python3
"""Module for Teacher class"""

from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String
from models.base_model import Base


@dataclass
class TeacherRecordSectionLink(Base):
    __tablename__ = "teacher_record_section_links"

    teacher_record_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("teacher_records.id"), primary_key=True
    )
    section_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("sections.id"), primary_key=True
    )
