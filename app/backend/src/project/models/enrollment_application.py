import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import UUID, DateTime, Enum, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin
from project.utils.enum import EnrollmentApplicationStatusEnum

if TYPE_CHECKING:
    from project.models.application_academic_background import ApplicationAcademicBackground
    from project.models.application_address import ApplicationAddress
    from project.models.application_health_records import ApplicationHealthRecord
    from project.models.enrollment_opportunity import EnrollmentOpportunity
    from project.models.school import School
    from project.models.user import User


class EnrollmentApplication(SchoolScopedMixin, BaseModel):
    __tablename__ = "enrollment_applications"

    applicant_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    student_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    opportunity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("enrollment_opportunities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[EnrollmentApplicationStatusEnum] = mapped_column(
        Enum(
            EnrollmentApplicationStatusEnum,
            name="enrollment_application_status_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=EnrollmentApplicationStatusEnum.SUBMITTED,
    )
    applicant_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)
    reviewer_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default_factory=lambda: datetime.now(timezone.utc),
    )
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_enrollment_application_id_school_id"),
        UniqueConstraint(
            "applicant_user_id",
            "student_user_id",
            "opportunity_id",
            name="uq_enrollment_applications_applicant_student_opp",
        ),
    )

    applicant_user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[applicant_user_id],
        back_populates="applicant_enrollment_applications",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    student_user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[student_user_id],
        back_populates="student_enrollment_applications",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    school: Mapped["School"] = relationship(
        "School",
        back_populates="enrollment_applications",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    opportunity: Mapped["EnrollmentOpportunity"] = relationship(
        "EnrollmentOpportunity",
        back_populates="applications",
        init=False,
        repr=False,
        passive_deletes=True,
    )

    health_record: Mapped["ApplicationHealthRecord"] = relationship(
        "ApplicationHealthRecord",
        back_populates="application",
        init=False,
        uselist=False,
    )
    academic_background: Mapped["ApplicationAcademicBackground"] = relationship(
        "ApplicationAcademicBackground",
        back_populates="application",
        init=False,
        uselist=False,
    )
    address: Mapped["ApplicationAddress"] = relationship(
        "ApplicationAddress",
        back_populates="application",
        init=False,
        uselist=False,
    )
