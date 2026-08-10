import uuid
from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import UUID, Date, Enum, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin
from project.utils.enum import JobStatusEnum

if TYPE_CHECKING:
    pass


class JobPosting(SchoolScopedMixin, BaseModel):
    """
    Represents a job posting in the system.
    """

    __tablename__ = "job_postings"

    position_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    employment_type: Mapped[str] = mapped_column(nullable=False)
    application_deadline: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    openings_count: Mapped[int] = mapped_column(nullable=False, default=1)
    allow_applications: Mapped[bool] = mapped_column(nullable=False, default=True)
    status: Mapped[JobStatusEnum] = mapped_column(
        Enum(
            JobStatusEnum,
            name="job_status_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=JobStatusEnum.PENDING,
    )

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_job_postings_id_school_id"),
        UniqueConstraint(
            "school_id",
            "position_id",
            name="uq_job_postings_school_id_position_id",
        ),
        ForeignKeyConstraint(
            ["position_id", "school_id"],
            ["positions.id", "positions.school_id"],
            name="fk_job_postings_position_id_school_id_positions",
        ),
    )
