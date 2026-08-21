import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    UUID,
    Boolean,
    Enum,
    ForeignKeyConstraint,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import TimestampMixin
from project.models.base.school_mixin import SchoolScopedMixin
from project.utils.enum import BloodTypeEnum

if TYPE_CHECKING:
    from project.models.enrollment_application import EnrollmentApplication


class ApplicationHealthRecord(SchoolScopedMixin, TimestampMixin):
    __tablename__ = "application_health_records"

    application_id: Mapped[uuid.UUID] = mapped_column(UUID(), primary_key=True, nullable=False)

    blood_type: Mapped[BloodTypeEnum] = mapped_column(
        Enum(
            BloodTypeEnum,
            name="blood_type_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=True,
        default=BloodTypeEnum.UNKNOWN,
    )
    has_disability: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    disability_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)
    has_medical_condition: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    medical_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)

    __table_args__ = (
        ForeignKeyConstraint(
            ["application_id", "school_id"],
            ["enrollment_applications.id", "enrollment_applications.school_id"],
            ondelete="CASCADE",
            name="fk_app_health_application",
        ),
        UniqueConstraint("school_id", "application_id", name="uq_school_app_health_per_application"),
    )

    application: Mapped["EnrollmentApplication"] = relationship(
        "EnrollmentApplication",
        back_populates="health_record",
        init=False,
        repr=False,
    )
