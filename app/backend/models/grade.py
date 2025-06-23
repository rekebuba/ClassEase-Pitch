#!/usr/bin/python3
"""Module for Grade class"""

from sqlalchemy import Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, scoped_session, Session
from models.base_model import BaseModel, CustomTypes
from typing import TYPE_CHECKING, List

from models.stream import Stream

if TYPE_CHECKING:
    from models.subject_grade_stream_link import SubjectGradeStreamLink
    from models.grade_stream_link import GradeStreamLink
    from models.stud_year_record import STUDYearRecord
    from models.section import Section
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
            level=CustomTypes.GradeLevelEnum.PRIMARY
            if i < 5
            else CustomTypes.GradeLevelEnum.MIDDLE_SCHOOL
            if i < 8
            else CustomTypes.GradeLevelEnum.HIGH_SCHOOL,
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
    level: Mapped[BaseModel.GradeLevelEnum] = mapped_column(
        Enum(
            BaseModel.GradeLevelEnum,
            name="grade_level_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )

    # Relationships
    sections: Mapped["Section"] = relationship(
        "Section",
        back_populates="grade",
        init=False,
    )

    streams: Mapped[List["Stream"]] = relationship(
        "Stream",
        back_populates="grades",
        secondary="grade_stream_links",
        init=False,
    )
    teachers: Mapped[List["Teacher"]] = relationship(
        "Teacher",
        back_populates="grade_level",
        secondary="teacher_grade_links",
        init=False,
    )
    subject_links: Mapped[List["SubjectGradeStreamLink"]] = relationship(
        "SubjectGradeStreamLink", back_populates="grade", init=False
    )
    student_year_records: Mapped[list["STUDYearRecord"]] = relationship(
        "STUDYearRecord", back_populates="grades", init=False
    )
