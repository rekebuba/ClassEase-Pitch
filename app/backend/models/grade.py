#!/usr/bin/python3
"""Module for Grade class"""

from sqlalchemy import Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, scoped_session, Session
from extension.enums.enum import GradeLevelEnum
from models.base_model import BaseModel
from typing import TYPE_CHECKING, List

from models.stream import Stream

if TYPE_CHECKING:
    from models.yearly_subject import YearlySubject
    from models.student_year_record import StudentYearRecord
    from models.teacher import Teacher


def seed_grades(session: scoped_session[Session]) -> None:
    """
    Populate the Grade table with default data (grades 1 to 12).

    This function checks if the Grade table is empty. If it is, it populates
    the table with grades from 1 to 12. If the table already contains data,
    the function does nothing.

    Args:
        session (Session): SQLAlchemy session object used to interact with the database.

    """
    # Check if the table is already populated
    if session.query(Grade).count() > 0:
        return

    social_stream = Stream(name="social")
    natural_stream = Stream(name="natural")

    for i in range(1, 13):
        grade = Grade(
            grade=i,
            level=GradeLevelEnum.PRIMARY
            if i < 5
            else GradeLevelEnum.MIDDLE_SCHOOL
            if i < 8
            else GradeLevelEnum.HIGH_SCHOOL,
        )

        if i > 10:
            # Assign streams to grades 11 and 12
            grade.streams = [social_stream, natural_stream]

        session.add(grade)

    session.commit()


class Grade(BaseModel):
    """Grade Model"""

    __tablename__ = "grades"

    # Database column
    grade: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
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
        back_populates="grade_level",
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
