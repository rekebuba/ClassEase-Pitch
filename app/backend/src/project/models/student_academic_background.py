import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import UUID, Boolean, ForeignKeyConstraint, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import TimestampMixin
from project.models.base.school_mixin import SchoolScopedMixin

if TYPE_CHECKING:
    from project.models.student import Student


class StudentAcademicBackground(SchoolScopedMixin, TimestampMixin):
    __tablename__ = "student_academic_backgrounds"

    student_id: Mapped[uuid.UUID] = mapped_column(UUID(), primary_key=True, nullable=False)

    previous_school: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_transfer: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ["student_id", "school_id"],
            ["students.id", "students.school_id"],
            ondelete="CASCADE",
            name="fk_app_bg_student",
        ),
        UniqueConstraint("school_id", "student_id", name="uq_school_app_bg_per_student"),
    )

    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="academic_background",
        init=False,
        repr=False,
    )
