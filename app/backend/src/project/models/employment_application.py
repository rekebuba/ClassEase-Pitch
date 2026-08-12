import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import UUID, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin
from project.utils.enum import EmploymentApplicationStatusEnum

if TYPE_CHECKING:
    from project.models.job_posting import JobPosting
    from project.models.school import School
    from project.models.user import User


class EmploymentApplication(SchoolScopedMixin, BaseModel):
    __tablename__ = "employment_applications"

    applicant_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    job_posting_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        nullable=False,
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
    cover_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)
    reviewer_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default_factory=lambda: datetime.now(timezone.utc),
    )
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_employment_application_id_school_id"),
        UniqueConstraint(
            "applicant_user_id",
            "job_posting_id",
            name="uq_employment_application_applicant_user_id_job_posting_id",
        ),
        ForeignKeyConstraint(
            ["job_posting_id", "school_id"],
            ["job_postings.id", "job_postings.school_id"],
            name="fk_employment_application_job_posting_id_school_id_job_postings",
        ),
    )

    applicant_user: Mapped["User"] = relationship(
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
    job_posting: Mapped["JobPosting"] = relationship(
        "JobPosting",
        back_populates="employment_applications",
        init=False,
        repr=False,
        passive_deletes=True,
    )
