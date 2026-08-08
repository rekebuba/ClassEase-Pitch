import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Dict, Optional

from sqlalchemy import JSON, UUID, DateTime, Enum, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin
from project.utils.enum import EmploymentApplicationStatusEnum

if TYPE_CHECKING:
    from project.models.employment_position import EmploymentPosition
    from project.models.employment_profile import EmploymentProfile
    from project.models.school import School
    from project.models.user import User


class EmploymentApplication(SchoolScopedMixin, BaseModel):
    __tablename__ = "employment_applications"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("employment_profiles.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    position_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("employment_positions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[EmploymentApplicationStatusEnum] = mapped_column(
        Enum(
            EmploymentApplicationStatusEnum,
            name="employment_application_status_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=EmploymentApplicationStatusEnum.SUBMITTED,
    )
    profile_snapshot: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default_factory=dict)
    applicant_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)
    reviewer_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default_factory=lambda: datetime.now(timezone.utc),
    )
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    withdrawn_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_employment_application_id_school_id"),
        UniqueConstraint("user_id", "position_id", name="uq_employment_application_user_position"),
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="employment_applications",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    school: Mapped["School"] = relationship(
        "School",
        back_populates="employment_applications",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    profile: Mapped["EmploymentProfile"] = relationship(
        "EmploymentProfile",
        back_populates="applications",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    position: Mapped["EmploymentPosition"] = relationship(
        "EmploymentPosition",
        back_populates="applications",
        init=False,
        repr=False,
        passive_deletes=True,
    )
