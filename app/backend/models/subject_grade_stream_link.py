#!/usr/bin/python3
"""Module for Subject class"""

from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel

if TYPE_CHECKING:
    from models.subject import Subject
    from models.grade import Grade
    from models.stream import Stream


class SubjectGradeStreamLink(BaseModel):
    __tablename__ = "subject_grade_stream_links"

    code: Mapped[str] = mapped_column(String(36), unique=True)
    subject_id: Mapped[str] = mapped_column(String(36), ForeignKey("subjects.id"))
    grade_id: Mapped[str] = mapped_column(String(36), ForeignKey("grades.id"))
    stream_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("streams.id"), nullable=True, default=None
    )

    # Optional: for bidirectional navigation
    subject: Mapped["Subject"] = relationship("Subject", init=False)
    grade: Mapped["Grade"] = relationship("Grade", init=False)
    stream: Mapped["Stream"] = relationship("Stream", init=False)
