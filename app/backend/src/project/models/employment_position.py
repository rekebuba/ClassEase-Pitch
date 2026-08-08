from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlalchemy import JSON, Boolean, DateTime, Enum, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin
from project.utils.enum import (
    EmploymentPositionStatusEnum,
    EmploymentPositionTypeEnum,
    PositionCategoryEnum,
)

if TYPE_CHECKING:
    from project.models.employment_application import EmploymentApplication
    from project.models.school import School


class EmploymentPosition(SchoolScopedMixin, BaseModel):
    __tablename__ = "employment_positions"

    title: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[PositionCategoryEnum] = mapped_column(
        Enum(
            PositionCategoryEnum,
            name="position_category_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=PositionCategoryEnum.OTHER,
    )
    employment_type: Mapped[EmploymentPositionTypeEnum] = mapped_column(
        Enum(
            EmploymentPositionTypeEnum,
            name="employment_position_type_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=EmploymentPositionTypeEnum.FULL_TIME,
    )
    status: Mapped[EmploymentPositionStatusEnum] = mapped_column(
        Enum(
            EmploymentPositionStatusEnum,
            name="employment_position_status_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=EmploymentPositionStatusEnum.DRAFT,
    )
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)
    requirements: Mapped[List[str]] = mapped_column(JSON, nullable=False, default_factory=list)
    responsibilities: Mapped[List[str]] = mapped_column(JSON, nullable=False, default_factory=list)
    benefits: Mapped[List[str]] = mapped_column(JSON, nullable=False, default_factory=list)
    location: Mapped[Optional[str]] = mapped_column(String(160), nullable=True, default=None)
    application_deadline: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )
    openings_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    allow_applications: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    extra: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default_factory=dict)

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_employment_position_id_school_id"),
        UniqueConstraint("school_id", "title", name="uq_employment_position_school_title"),
    )

    school: Mapped[Optional["School"]] = relationship(
        "School",
        back_populates="employment_positions",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    applications: Mapped[List["EmploymentApplication"]] = relationship(
        "EmploymentApplication",
        back_populates="position",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    @property
    def is_open(self) -> bool:
        if self.status != EmploymentPositionStatusEnum.OPEN or not self.allow_applications:
            return False
        if self.application_deadline is None:
            return True
        return self.application_deadline >= datetime.now(self.application_deadline.tzinfo)
