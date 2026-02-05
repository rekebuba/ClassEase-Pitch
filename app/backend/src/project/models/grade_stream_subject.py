import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import UUID, ForeignKey, UniqueConstraint
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.utils.utils import sort_grade_key

if TYPE_CHECKING:
    from project.models.grade import Grade
    from project.models.stream import Stream
    from project.models.subject import Subject
    from project.models.teacher_record import TeacherRecord


class GradeStreamSubject(BaseModel):
    """
    Association object linking Grade, Stream, and Subject.
    Stream can be NULL for grades without streams.
    """

    __tablename__ = "grade_stream_subjects"

    grade_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("grades.id", ondelete="CASCADE"),
        nullable=False,
    )
    stream_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(),
        ForeignKey("streams.id", ondelete="CASCADE"),
        nullable=True,
    )
    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("subjects.id", ondelete="CASCADE"),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "grade_id",
            "stream_id",
            "subject_id",
            name="uq_grade_stream_subject",
        ),
    )

    # Many-To-One Relationships
    grade: Mapped[Optional["Grade"]] = relationship(
        "Grade",
        back_populates="grade_stream_subjects",
        init=False,
        passive_deletes=True,
        repr=False,
    )
    stream: Mapped[Optional["Stream"]] = relationship(
        "Stream",
        back_populates="grade_stream_subjects",
        passive_deletes=True,
        init=False,
        repr=False,
    )
    subject: Mapped["Subject"] = relationship(
        "Subject",
        back_populates="grade_stream_subjects",
        passive_deletes=True,
        init=False,
        repr=False,
    )

    # One-To-Many Relationships
    teacher_records: Mapped[List["TeacherRecord"]] = relationship(
        "TeacherRecord",
        back_populates="grade_stream_subject",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    _teacher_grades: AssociationProxy[List["Grade"]] = association_proxy(
        "teacher_records",
        "grade",
        default_factory=list,
    )

    @property
    def teacher_grades(self) -> List["Grade"]:
        """Return unique teacher grades that have streams assigned to this subject."""
        seen = set()
        result = []
        for g in self._teacher_grades:
            if g is not None and g.id not in seen:
                seen.add(g.id)
                result.append(g)
        return sorted(result, key=sort_grade_key)

    _teacher_subjects: AssociationProxy[List["Subject"]] = association_proxy(
        "teacher_records",
        "subject",
        default_factory=list,
    )

    @property
    def teacher_subjects(self) -> List["Subject"]:
        """Return unique, non-null teacher_subjects."""
        seen = set()
        result = []
        for s in self._teacher_subjects:
            if s is not None and s.id not in seen:
                seen.add(s.id)
                result.append(s)

        return sorted(result, key=lambda x: x.name)
