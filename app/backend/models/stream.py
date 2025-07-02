#!/usr/bin/python3
"""Module for Subject class"""

from typing import TYPE_CHECKING, List
from sqlalchemy import String
from models.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.yearly_subject import YearlySubject
    from models.grade import Grade


class Stream(BaseModel):
    __tablename__ = "streams"

    name: Mapped[str] = mapped_column(String(10), nullable=False)

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
