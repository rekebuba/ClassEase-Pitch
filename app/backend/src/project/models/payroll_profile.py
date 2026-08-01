import uuid
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    UUID,
    Boolean,
    CheckConstraint,
    Enum,
    ForeignKeyConstraint,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin
from project.utils.enum import PayrollPayFrequencyEnum, PayrollPaymentMethodEnum

if TYPE_CHECKING:
    from project.models.employee import Employee
    from project.models.school import School


class PayrollProfile(SchoolScopedMixin, BaseModel):
    __tablename__ = "payroll_profiles"

    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    tax_identifier: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        default=None,
    )
    bank_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        default=None,
    )
    bank_account: Mapped[Optional[str]] = mapped_column(
        String(120),
        nullable=True,
        default=None,
    )
    payment_method: Mapped[PayrollPaymentMethodEnum] = mapped_column(
        Enum(
            PayrollPaymentMethodEnum,
            name="payroll_payment_method_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=PayrollPaymentMethodEnum.BANK_TRANSFER,
    )
    base_salary: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
    )
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")
    pay_frequency: Mapped[PayrollPayFrequencyEnum] = mapped_column(
        Enum(
            PayrollPayFrequencyEnum,
            name="payroll_pay_frequency_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=PayrollPayFrequencyEnum.MONTHLY,
    )
    overtime_eligible: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_payroll_profile_id_school_id"),
        UniqueConstraint(
            "school_id",
            "employee_id",
            name="uq_payroll_profile_school_employee",
        ),
        CheckConstraint("base_salary >= 0", name="check_payroll_profile_base_salary"),
        ForeignKeyConstraint(
            ["employee_id", "school_id"],
            ["employees.id", "employees.school_id"],
            name="fk_payroll_profile_employee_school",
            ondelete="CASCADE",
        ),
    )

    school: Mapped[Optional["School"]] = relationship(
        "School",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="payroll_profile",
    )
    employee: Mapped["Employee"] = relationship(
        "Employee",
        back_populates="payroll_profile",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="school",
    )
