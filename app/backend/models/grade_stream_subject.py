import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base.base_model import BaseModel
from models.base.column_type import UUIDType

if TYPE_CHECKING:
    from models.grade import Grade
    from models.stream import Stream
    from models.subject import Subject
    from models.teacher_record import TeacherRecord


class GradeStreamSubject(BaseModel):
    """
    Association object linking Grade, Stream, and Subject.
    Stream can be NULL for grades without streams.
    """

    __tablename__ = "grade_stream_subjects"

    grade_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
        ForeignKey("grades.id", ondelete="CASCADE"),
        nullable=False,
    )
    stream_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUIDType(),
        ForeignKey("streams.id", ondelete="CASCADE"),
        nullable=True,
    )
    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(),
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
