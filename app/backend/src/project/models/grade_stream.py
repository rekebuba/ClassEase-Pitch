"""Module for SubjectOffering class"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import UUID, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin

if TYPE_CHECKING:
    from project.models.class_section import ClassSection
    from project.models.grade import Grade
    from project.models.stream import Stream
    from project.models.subject_offering import SubjectOffering


class GradeStream(SchoolScopedMixin, BaseModel):
    """
    Represents a grade stream in the system.
    """

    __tablename__ = "grade_streams"

    grade_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    stream_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(),
        nullable=True,
        default=None,
    )

    # Relationships
    grade: Mapped["Grade"] = relationship(
        "Grade",
        back_populates="grade_streams",
        init=False,
        repr=False,
        overlaps="grade_streams,stream",
    )
    stream: Mapped[Optional["Stream"]] = relationship(
        "Stream",
        back_populates="grade_streams",
        init=False,
        repr=False,
        overlaps="grade,grade_streams",
    )
    class_sections: Mapped[list["ClassSection"]] = relationship(
        "ClassSection",
        back_populates="grade_stream",
        default_factory=list,
        repr=False,
        overlaps="academic_year,class_sections,grade_stream,homeroom_teacher,school,section",
    )

    subject_offerings: Mapped[list["SubjectOffering"]] = relationship(
        "SubjectOffering",
        back_populates="grade_stream",
        default_factory=list,
        repr=False,
        overlaps="assessment_scheme,grade_stream,school,subject_offerings",
    )

    subjects = association_proxy("subject_offerings", "subject")

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_grade_stream_id_school_id"),
        UniqueConstraint("grade_id", "stream_id", "school_id", name="uq_grade_stream_grade_stream_school"),
        ForeignKeyConstraint(
            ["grade_id", "school_id"],
            ["grades.id", "grades.school_id"],
            name="fk_grade_stream_grade_school",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["stream_id", "school_id"],
            ["streams.id", "streams.school_id"],
            name="fk_grade_stream_stream_school",
            ondelete="CASCADE",
        ),
    )
