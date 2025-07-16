#!/usr/bin/python3
"""Module for Teacher class"""

from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from models.base.base_model import Base
from models.base.column_type import UUIDType
import uuid


@dataclass
class TeacherYearlySubjectLink(Base):
    __tablename__ = "teacher_yearly_subject_links"

    teacher_record_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("teacher_records.id"),
        primary_key=True,
    )
    yearly_subject_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("yearly_subjects.id"),
        primary_key=True,
    )
