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
    year_id: Mapped[uuid.UUID] = mapped_column(UUIDType(), ForeignKey("years.id", ondelete='CASCADE'))
    subject_id: Mapped[uuid.UUID] = mapped_column(UUIDType(), ForeignKey("subjects.id", ondelete='CASCADE'))
    grade_id: Mapped[uuid.UUID] = mapped_column(UUIDType(), ForeignKey("grades.id", ondelete='CASCADE'))
    stream_id: Mapped[Optional[str]] = mapped_column(
        UUIDType(),
        ForeignKey("streams.id", ondelete='CASCADE'),
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
