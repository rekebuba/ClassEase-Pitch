import uuid
from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    UUID,
    CheckConstraint,
    Date,
    Enum,
    ForeignKeyConstraint,
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin
from project.utils.enum import ContractStatusEnum, ContractTypeEnum

if TYPE_CHECKING:
    from project.models.employee import Employee
    from project.models.school import School


class EmploymentContract(SchoolScopedMixin, BaseModel):
    __tablename__ = "employment_contracts"

    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    contract_type: Mapped[ContractTypeEnum] = mapped_column(
        Enum(
            ContractTypeEnum,
            name="contract_type_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )
    hours_per_week: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, default=None)
    status: Mapped[ContractStatusEnum] = mapped_column(
        Enum(
            ContractStatusEnum,
            name="contract_status_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=ContractStatusEnum.DRAFT,
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["employee_id", "school_id"],
            ["employees.id", "employees.school_id"],
            name="fk_employment_contract_employee_school",
            ondelete="CASCADE",
        ),
        CheckConstraint(
            "end_date IS NULL OR end_date >= start_date",
            name="check_employment_contract_dates",
        ),
        CheckConstraint(
            "hours_per_week > 0",
            name="check_employment_contract_hours_per_week",
        ),
    )

    school: Mapped[Optional["School"]] = relationship(
        "School",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="employment_contracts",
    )
    employee: Mapped["Employee"] = relationship(
        "Employee",
        back_populates="employment_contracts",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="school",
    )
