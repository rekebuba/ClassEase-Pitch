import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKeyConstraint, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import TimestampMixin
from project.models.base.school_mixin import SchoolScopedMixin

if TYPE_CHECKING:
    from project.models.student import Student


class StudentAddress(SchoolScopedMixin, TimestampMixin):
    __tablename__ = "student_addresses"

    student_id: Mapped[uuid.UUID] = mapped_column(UUID(), primary_key=True, nullable=False)

    nationality: Mapped[str] = mapped_column(String(100), nullable=True)
    city: Mapped[str] = mapped_column(String(50), nullable=True)
    state: Mapped[str] = mapped_column(String(50), nullable=True)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=True)
    transportation: Mapped[str] = mapped_column(String(50), nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["student_id", "school_id"],
            ["students.id", "students.school_id"],
            ondelete="CASCADE",
            name="fk_app_addresses_student",
        ),
        UniqueConstraint("school_id", "student_id", name="uq_school_app_addresses_per_student"),
    )

    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="address",
        init=False,
        repr=False,
    )
