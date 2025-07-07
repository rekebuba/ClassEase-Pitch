#!/usr/bin/python3
"""Module for Grade class"""

from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extension.enums.enum import GradeLevelEnum
from models.base_model import BaseModel
from typing import TYPE_CHECKING, List

from models.stream import Stream

if TYPE_CHECKING:
    from models.yearly_subject import YearlySubject
    from models.student_year_record import StudentYearRecord
    from models.teacher import Teacher


class Grade(BaseModel):
    """Grade Model"""

    __tablename__ = "grades"

    # Database column
    grade: Mapped[str] = mapped_column(
        String(25), unique=True, nullable=False, index=True
    )
    level: Mapped[GradeLevelEnum] = mapped_column(
        Enum(
            GradeLevelEnum,
            name="grade_level_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )

    # Relationships
    streams: Mapped[List["Stream"]] = relationship(
        "Stream",
        back_populates="grades",
        secondary="grade_stream_links",
        repr=False,
        default_factory=list,
    )
    teachers: Mapped[List["Teacher"]] = relationship(
        "Teacher",
        back_populates="grade_to_teach",
        secondary="teacher_grade_links",
        repr=False,
        default_factory=list,
    )
    yearly_subjects: Mapped[List["YearlySubject"]] = relationship(
        "YearlySubject",
        back_populates="grade",
        repr=False,
        default_factory=list,
    )
    student_year_records: Mapped[list["StudentYearRecord"]] = relationship(
        "StudentYearRecord",
        back_populates="grade",
        repr=False,
        default_factory=list,
    )
