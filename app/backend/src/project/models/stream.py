#!/usr/bin/python3
"""Module for Stream class"""

from typing import TYPE_CHECKING, List

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin

if TYPE_CHECKING:
    from project.models.grade_stream import GradeStream
    from project.models.school import School


class Stream(SchoolScopedMixin, BaseModel):
    __tablename__ = "streams"

    name: Mapped[str] = mapped_column(String(50), nullable=False)

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_stream_id_school_id"),
        UniqueConstraint("name", "school_id", name="uq_stream_name_school_id"),
    )

    school: Mapped["School"] = relationship(
        "School",
        back_populates="streams",
        init=False,
        repr=False,
        overlaps="school,grade,stream,streams,subject,subject_offerings,year",
    )
    grade_streams: Mapped[List["GradeStream"]] = relationship(
        "GradeStream",
        back_populates="stream",
        default_factory=list,
        repr=False,
        overlaps="grade_streams",
    )
