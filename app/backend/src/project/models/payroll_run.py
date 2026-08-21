import uuid
from datetime import date
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    UUID,
    CheckConstraint,
    Date,
    Enum,
    ForeignKeyConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin
from project.utils.enum import PayrollRunStatusEnum

if TYPE_CHECKING:
    from project.models.employee import Employee
    from project.models.payroll_entry import PayrollEntry
    from project.models.school import School


class PayrollRun(SchoolScopedMixin, BaseModel):
    __tablename__ = "payroll_runs"

    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[PayrollRunStatusEnum] = mapped_column(
        Enum(
            PayrollRunStatusEnum,
            name="payroll_run_status_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=PayrollRunStatusEnum.DRAFT,
    )
    processed_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(),
        nullable=True,
        default=None,
    )

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_payroll_run_id_school_id"),
        UniqueConstraint(
            "school_id",
            "period_start",
            "period_end",
            name="uq_payroll_run_school_period",
        ),
        CheckConstraint("period_end >= period_start", name="check_payroll_run_dates"),
        ForeignKeyConstraint(
            ["processed_by", "school_id"],
            ["employees.id", "employees.school_id"],
            name="fk_payroll_run_processed_by_school",
            ondelete="SET NULL",
        ),
    )

    school: Mapped[Optional["School"]] = relationship(
        "School",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    processor: Mapped[Optional["Employee"]] = relationship(
        "Employee",
        foreign_keys=[processed_by],
        back_populates="processed_payroll_runs",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    payroll_entries: Mapped[List["PayrollEntry"]] = relationship(
        "PayrollEntry",
        back_populates="payroll_run",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="employee,payroll_entries,school",
    )
