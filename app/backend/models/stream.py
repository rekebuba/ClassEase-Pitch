#!/usr/bin/python3
"""Module for Subject class"""

from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey, String
from models.base.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship


from models.base.column_type import UUIDType
import uuid


if TYPE_CHECKING:
    from models.yearly_subject import YearlySubject
    from models.grade import Grade
    from models.subject import Subject
    from models.student import Student


class Stream(BaseModel):
    __tablename__ = "streams"

    grade_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("grades.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(10), nullable=False)

    # One-To-Many Relationships
    grade: Mapped["Grade"] = relationship(
        "Grade",
        back_populates="streams",
        repr=False,
        init=False,
    )
    yearly_subjects: Mapped[List["YearlySubject"]] = relationship(
        "YearlySubject",
        back_populates="stream",
        repr=False,
        default_factory=list,
    )
    subjects: Mapped[List["Subject"]] = relationship(
        "Subject",
        back_populates="streams",
        secondary="subject_stream_links",
        default_factory=list,
        repr=False,
    )

    students: Mapped[List["Student"]] = relationship(
        "Student",
        secondary="student_stream_links",
        back_populates="streams",
        default_factory=list,
        repr=False,
    )
