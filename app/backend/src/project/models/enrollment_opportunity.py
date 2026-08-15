import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import UUID, Boolean, DateTime, Enum, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin
from project.utils.enum import EnrollmentOpportunityStatusEnum

if TYPE_CHECKING:
    from project.models.enrollment_application import EnrollmentApplication
    from project.models.grade_stream import GradeStream
    from project.models.school import School
    from project.models.year import Year


class EnrollmentOpportunity(SchoolScopedMixin, BaseModel):
    __tablename__ = "enrollment_opportunities"

    academic_year_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("years.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    grade_stream_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("grade_streams.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[EnrollmentOpportunityStatusEnum] = mapped_column(
        Enum(
            EnrollmentOpportunityStatusEnum,
            name="enrollment_opportunity_status_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=EnrollmentOpportunityStatusEnum.OPEN,
    )
    application_deadline: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )
    capacity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    allow_applications: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_enrollment_opportunity_id_school_id"),
        UniqueConstraint(
            "school_id",
            "academic_year_id",
            "grade_stream_id",
            name="uq_enrollment_opportunity_school_year_grade_stream",
        ),
    )

    school: Mapped[Optional["School"]] = relationship(
        "School",
        back_populates="enrollment_opportunities",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    academic_year: Mapped["Year"] = relationship(
        "Year",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    grade_stream: Mapped["GradeStream"] = relationship(
        "GradeStream",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    applications: Mapped[list["EnrollmentApplication"]] = relationship(
        "EnrollmentApplication",
        back_populates="opportunity",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    @property
    def is_open(self) -> bool:
        if self.status != EnrollmentOpportunityStatusEnum.OPEN or not self.allow_applications:
            return False
        if self.application_deadline is None:
            return True
        return self.application_deadline >= datetime.now(self.application_deadline.tzinfo)
