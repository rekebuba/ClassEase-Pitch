#!/usr/bin/python3
"""Module for Subject class"""

from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.assessment import Assessment
from models.base_model import BaseModel

if TYPE_CHECKING:
    from models.teacher_record import TeachersRecord
    from models.subject_yearly_average import SubjectYearlyAverage
    from models.subject import Subject
    from models.grade import Grade
    from models.stream import Stream
    from models.year import Year
    from models.section import Section


class YearlySubject(BaseModel):
    __tablename__ = "yearly_subjects"

    subject_code: Mapped[str] = mapped_column(String(25), nullable=False)
    year_id: Mapped[str] = mapped_column(String(36), ForeignKey("years.id"))
    subject_id: Mapped[str] = mapped_column(String(36), ForeignKey("subjects.id"))
    grade_id: Mapped[str] = mapped_column(String(36), ForeignKey("grades.id"))
    stream_id: Mapped[Optional[str]] = mapped_column(
        String(36),
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

    # Many-to-many relationships
    teacher_records_link: Mapped[List["TeachersRecord"]] = relationship(
        "TeachersRecord",
        back_populates="yearly_subjects_link",
        secondary="teacher_yearly_subject_links",
        default_factory=list,
        repr=False,
    )
