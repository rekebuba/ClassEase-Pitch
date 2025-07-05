#!/usr/bin/python3
"""Module for Teacher class"""

from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String
from models.base_model import Base


@dataclass
class TeacherYearlySubjectLink(Base):
    __tablename__ = "teacher_yearly_subject_links"

    teacher_record_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("teacher_records.id"), primary_key=True
    )
    yearly_subject_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("yearly_subjects.id"), primary_key=True
    )
