#!/usr/bin/python3
"""Module for Grade class"""

from typing import TYPE_CHECKING, List

from sqlalchemy import Enum, UniqueConstraint
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin
from project.utils.enum import GradeEnum, GradeLevelEnum

if TYPE_CHECKING:
    from project.models.grade_stream import GradeStream
    from project.models.section import Section


class Grade(SchoolScopedMixin, BaseModel):
    """Grade Model"""

    __tablename__ = "grades"

    # Database column
    grade: Mapped[GradeEnum] = mapped_column(
        Enum(
            GradeEnum,
            name="grade_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )
    level: Mapped[GradeLevelEnum] = mapped_column(
        Enum(
            GradeLevelEnum,
            name="grade_level_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )
    has_stream: Mapped[bool] = mapped_column(nullable=False, default=False)

    __table_args__ = (UniqueConstraint("id", "school_id", name="uq_grade_id_school_id"),)

    # One-To-Many Relationships
    sections: Mapped[List["Section"]] = relationship(
        "Section",
        back_populates="grade",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    grade_streams: Mapped[List["GradeStream"]] = relationship(
        "GradeStream",
        back_populates="grade",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    subjects = association_proxy("subject_offerings", "subject")
    streams = association_proxy("grade_streams", "stream")
