#!/usr/bin/python3
"""Module for Subject class"""

from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey, String
from models.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.year import Year


if TYPE_CHECKING:
    from models.yearly_subject import YearlySubject
    from models.grade import Grade
    from models.student_year_record import StudentYearRecord


class Stream(BaseModel):
    __tablename__ = "streams"

    year_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("years.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(10), nullable=False)

    # Relationships
    year: Mapped["Year"] = relationship(
        "Year",
        back_populates="streams",
        repr=False,
        init=False,
    )
    grades: Mapped[List["Grade"]] = relationship(
        "Grade",
        back_populates="streams",
        secondary="grade_stream_links",
        repr=False,
        default_factory=list,
    )
    yearly_subjects: Mapped[List["YearlySubject"]] = relationship(
        "YearlySubject",
        back_populates="stream",
        repr=False,
        default_factory=list,
    )
    students: Mapped[List["StudentYearRecord"]] = relationship(
        "StudentYearRecord",
        back_populates="stream",
        repr=False,
        default_factory=list,
    )
