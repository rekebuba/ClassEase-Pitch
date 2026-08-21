import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import UUID, Boolean, ForeignKeyConstraint, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import TimestampMixin
from project.models.base.school_mixin import SchoolScopedMixin

if TYPE_CHECKING:
    from project.models.enrollment_application import EnrollmentApplication


class ApplicationAcademicBackground(SchoolScopedMixin, TimestampMixin):
    __tablename__ = "application_academic_backgrounds"

    application_id: Mapped[uuid.UUID] = mapped_column(UUID(), primary_key=True, nullable=False)

    previous_school: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_transfer: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ["application_id", "school_id"],
            ["enrollment_applications.id", "enrollment_applications.school_id"],
            ondelete="CASCADE",
            name="fk_app_bg_application",
        ),
        UniqueConstraint("school_id", "application_id", name="uq_school_app_bg_per_application"),
    )
    # Exclude inherited 'id' column from this model's mapping
    __mapper_args__ = {"exclude_properties": ["id"]}

    application: Mapped["EnrollmentApplication"] = relationship(
        "EnrollmentApplication",
        back_populates="academic_background",
        init=False,
        repr=False,
    )
