#!/usr/bin/python3
"""Module for Teacher class"""

import uuid
from dataclasses import dataclass

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base.base_model import Base
from models.base.column_type import UUIDType


@dataclass
class TeacherSubjectLink(Base):
    __tablename__ = "teacher_subject_links"

    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("teachers.id", ondelete="CASCADE"),
        primary_key=True,
    )
    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("subjects.id", ondelete="CASCADE"),
        primary_key=True,
    )
