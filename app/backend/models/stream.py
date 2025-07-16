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
    from models.student_year_record import StudentYearRecord
    from models.subject import Subject
    from models.year import Year


class Stream(BaseModel):
    __tablename__ = "streams"

    year_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("years.id"), nullable=False, index=True
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
    subject_links: Mapped[List["Subject"]] = relationship(
        "Subject",
        back_populates="stream_links",
        secondary="subject_stream_links",
        default_factory=list,
        repr=False,
    )
