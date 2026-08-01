#!/usr/bin/python3
"""Module for Stream class"""

import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import UUID, ForeignKeyConstraint, String, UniqueConstraint
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin

if TYPE_CHECKING:
    from project.models.grade import Grade
    from project.models.school import School
    from project.models.subject import Subject
    from project.models.subject_offering import SubjectOffering


class Stream(SchoolScopedMixin, BaseModel):
    __tablename__ = "streams"

    grade_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_stream_id_school_id"),
        UniqueConstraint("grade_id", "name", name="uq_grade_name"),
        ForeignKeyConstraint(
            ["grade_id", "school_id"],
            ["grades.id", "grades.school_id"],
            name="fk_stream_grade_school",
            ondelete="CASCADE",
        ),
    )

    school: Mapped["School"] = relationship(
        "School",
        back_populates="streams",
        init=False,
        repr=False,
        overlaps="school,grade,stream,streams,subject,subject_offerings,year",
    )
    grade: Mapped["Grade"] = relationship(
        "Grade",
        back_populates="streams",
        repr=False,
        passive_deletes=True,
        init=False,
    )
    subject_offerings: Mapped[List["SubjectOffering"]] = relationship(
        "SubjectOffering",
        back_populates="stream",
        default_factory=list,
        repr=False,
        overlaps="subject_offerings",
    )

    # Association proxy
    subjects: AssociationProxy[List["Subject"]] = association_proxy(
        "subject_offerings",
        "subject",
        default_factory=list,
    )
