#!/usr/bin/python3
"""Module for Subject class"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.assessment import Assessment
from models.base_model import BaseModel

if TYPE_CHECKING:
    from models.subject import Subject
    from models.grade import Grade
    from models.stream import Stream
    from models.year import Year


class YearlySubject(BaseModel):
    __tablename__ = "yearly_subjects"

    year_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("years.id"))
    subject_id: Mapped[str] = mapped_column(String(36), ForeignKey("subjects.id"))
    grade_id: Mapped[str] = mapped_column(String(36), ForeignKey("grades.id"))
    stream_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("streams.id"), nullable=True, default=None
    )

    # Relationships
    year: Mapped["Year"] = relationship(
        "Year",
        back_populates="yearly_subjects",
        init=False,
        repr=False,
    )

    subject: Mapped["Subject"] = relationship(
        "Subject",
        back_populates="yearly_subjects",
        init=False,
        repr=False,
    )
    grade: Mapped["Grade"] = relationship(
        "Grade",
        back_populates="yearly_subjects",
        init=False,
        repr=False,
    )
    stream: Mapped["Stream"] = relationship(
        "Stream",
        back_populates="yearly_subjects",
        init=False,
        repr=False,
    )
    assessments: Mapped[List["Assessment"]] = relationship(  # noqa: F821
        "Assessment",
        back_populates="yearly_subject",
        default_factory=list,
        repr=False,
    )
