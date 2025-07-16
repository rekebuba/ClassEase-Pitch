#!/usr/bin/python3
"""Module for Teacher class"""

from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from models.base.base_model import Base
from models.base.column_type import UUIDType
import uuid


@dataclass
class TeacherRecordSectionLink(Base):
    __tablename__ = "teacher_record_section_links"

    teacher_record_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("teacher_records.id"), primary_key=True
    )
    section_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("sections.id"), primary_key=True
    )
