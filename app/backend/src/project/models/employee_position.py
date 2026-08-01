import uuid
from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    UUID,
    Boolean,
    CheckConstraint,
    Date,
    ForeignKeyConstraint,
    Index,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin

if TYPE_CHECKING:
    from project.models.employee import Employee
    from project.models.position import Position
    from project.models.school import School


class EmployeePosition(SchoolScopedMixin, BaseModel):
    __tablename__ = "employee_positions"

    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    position_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, default=None)
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_employee_position_id_school_id"),
        CheckConstraint(
            "end_date IS NULL OR end_date >= start_date",
            name="check_employee_position_dates",
        ),
        ForeignKeyConstraint(
            ["employee_id", "school_id"],
            ["employees.id", "employees.school_id"],
            name="fk_employee_position_employee_school",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["position_id", "school_id"],
            ["positions.id", "positions.school_id"],
            name="fk_employee_position_position_school",
            ondelete="RESTRICT",
        ),
        Index(
            "uq_employee_one_active_primary_position",
            "employee_id",
            unique=True,
            postgresql_where=text("is_primary = true AND end_date IS NULL"),
        ),
    )

    school: Mapped[Optional["School"]] = relationship(
        "School",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="employee_positions",
    )
    employee: Mapped["Employee"] = relationship(
        "Employee",
        back_populates="employee_positions",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="school",
    )
    position: Mapped["Position"] = relationship(
        "Position",
        back_populates="employee_positions",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="employee,employee_positions,school",
    )
