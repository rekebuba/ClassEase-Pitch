#!/usr/bin/python3
"""Module for Subject class"""

from typing import TYPE_CHECKING, List, Optional
import uuid
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.assessment import Assessment
from models.base.base_model import BaseModel
from models.base.column_type import UUIDType

if TYPE_CHECKING:
    from models.subject_yearly_average import SubjectYearlyAverage
    from models.subject import Subject
    from models.grade import Grade
    from models.stream import Stream
    from models.year import Year


class YearlySubject(BaseModel):
    __tablename__ = "yearly_subjects"

    subject_code: Mapped[str] = mapped_column(String(25), nullable=False)
    year_id: Mapped[uuid.UUID] = mapped_column(UUIDType(), ForeignKey("years.id"))
    subject_id: Mapped[uuid.UUID] = mapped_column(UUIDType(), ForeignKey("subjects.id"))
    grade_id: Mapped[uuid.UUID] = mapped_column(UUIDType(), ForeignKey("grades.id"))
    stream_id: Mapped[Optional[str]] = mapped_column(
        UUIDType(),
        ForeignKey("streams.id"),
        nullable=True,
        default=None,
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
    assessments: Mapped[List["Assessment"]] = relationship(
        "Assessment",
        back_populates="yearly_subject",
        default_factory=list,
        repr=False,
    )
    subject_yearly_averages: Mapped[List["SubjectYearlyAverage"]] = relationship(
        "SubjectYearlyAverage",
        back_populates="yearly_subject",
        default_factory=list,
        repr=False,
    )
