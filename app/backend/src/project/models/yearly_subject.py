#!/usr/bin/python3
"""Module for Subject class"""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.assessment import Assessment
from project.models.base.base_model import BaseModel
from sqlalchemy import UUID

if TYPE_CHECKING:
    from project.models.grade import Grade
    from project.models.stream import Stream
    from project.models.subject import Subject
    from project.models.subject_yearly_average import SubjectYearlyAverage
    from project.models.year import Year


class YearlySubject(BaseModel):
    __tablename__ = "yearly_subjects"

    subject_code: Mapped[str] = mapped_column(String(25), nullable=False)
    year_id: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("years.id", ondelete="CASCADE")
    )
    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("subjects.id", ondelete="CASCADE")
    )
    grade_id: Mapped[uuid.UUID] = mapped_column(
        UUID(), ForeignKey("grades.id", ondelete="CASCADE")
    )
    stream_id: Mapped[Optional[str]] = mapped_column(
        UUID(),
        ForeignKey("streams.id", ondelete="CASCADE"),
        nullable=True,
        default=None,
    )

    # Relationships

    assessments: Mapped[List["Assessment"]] = relationship(
        "Assessment",
        back_populates="yearly_subject",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    subject_yearly_averages: Mapped[List["SubjectYearlyAverage"]] = relationship(
        "SubjectYearlyAverage",
        back_populates="yearly_subject",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
