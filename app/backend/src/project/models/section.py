#!/usr/bin/python3
"""Module for Section class"""

import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import UUID, ForeignKeyConstraint, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin

if TYPE_CHECKING:
    from project.models.class_section import ClassSection
    from project.models.grade import Grade


class Section(SchoolScopedMixin, BaseModel):
    """
    Represents a section within a grade.
    """

    __tablename__ = "sections"
    grade_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        nullable=False,
        index=True,
    )
    section: Mapped[str] = mapped_column(
        String(1),
        nullable=True,
    )  # e.g., A, B, C, D, E, F, G

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_section_id_school_id"),
        UniqueConstraint("grade_id", "section", name="uq_section_grade_section"),
        ForeignKeyConstraint(
            ["grade_id", "school_id"],
            ["grades.id", "grades.school_id"],
            name="fk_section_grade_school",
            ondelete="CASCADE",
        ),
    )

    # Relationships
    grade: Mapped["Grade"] = relationship(
        "Grade",
        back_populates="sections",
        repr=False,
        passive_deletes=True,
        init=False,
    )

    class_sections: Mapped[List["ClassSection"]] = relationship(
        "ClassSection",
        back_populates="section",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="academic_year,grade,homeroom_teacher,school",
    )
