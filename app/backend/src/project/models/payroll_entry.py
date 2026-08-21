import uuid
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    UUID,
    CheckConstraint,
    ForeignKeyConstraint,
    Numeric,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin

if TYPE_CHECKING:
    from project.models.employee import Employee
    from project.models.payroll_run import PayrollRun
    from project.models.school import School


class PayrollEntry(SchoolScopedMixin, BaseModel):
    __tablename__ = "payroll_entries"

    payroll_run_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    base_salary: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
    )
    allowances: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
    )
    deductions: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
    )
    overtime: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
    )
    bonuses: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
    )
    tax: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
    )
    net_pay: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
    )

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_payroll_entry_id_school_id"),
        UniqueConstraint(
            "school_id",
            "payroll_run_id",
            "employee_id",
            name="uq_payroll_entry_run_employee",
        ),
        ForeignKeyConstraint(
            ["payroll_run_id", "school_id"],
            ["payroll_runs.id", "payroll_runs.school_id"],
            name="fk_payroll_entry_run_school",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["employee_id", "school_id"],
            ["employees.id", "employees.school_id"],
            name="fk_payroll_entry_employee_school",
            ondelete="CASCADE",
        ),
        CheckConstraint("base_salary >= 0", name="check_payroll_entry_base_salary"),
        CheckConstraint("allowances >= 0", name="check_payroll_entry_allowances"),
        CheckConstraint("deductions >= 0", name="check_payroll_entry_deductions"),
        CheckConstraint("overtime >= 0", name="check_payroll_entry_overtime"),
        CheckConstraint("bonuses >= 0", name="check_payroll_entry_bonuses"),
        CheckConstraint("tax >= 0", name="check_payroll_entry_tax"),
        CheckConstraint("net_pay >= 0", name="check_payroll_entry_net_pay"),
    )

    school: Mapped[Optional["School"]] = relationship(
        "School",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="payroll_entries",
    )
    payroll_run: Mapped["PayrollRun"] = relationship(
        "PayrollRun",
        back_populates="payroll_entries",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="payroll_entries,school",
    )
    employee: Mapped["Employee"] = relationship(
        "Employee",
        back_populates="payroll_entries",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="payroll_run,school",
    )
