#!/usr/bin/python3
"""Module for Subject class"""

from typing import TYPE_CHECKING, List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel
from models.yearly_subject import YearlySubject

if TYPE_CHECKING:
    from models.teacher import Teacher
    from models.year import Year


class Subject(BaseModel):
    """
    Subject Model
    """

    __tablename__ = "subjects"
    year_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("years.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    code: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)

    # Relationships
    year: Mapped["Year"] = relationship(
        "Year",
        back_populates="subjects",
        repr=False,
        init=False,
    )
    teachers: Mapped[List["Teacher"]] = relationship(
        "Teacher",
        back_populates="subjects_to_teach",
        secondary="teacher_subject_links",
        default_factory=list,
        repr=False,
    )
    yearly_subjects: Mapped[List["YearlySubject"]] = relationship(
        "YearlySubject",
        back_populates="subject",
        default_factory=list,
        repr=False,
    )
