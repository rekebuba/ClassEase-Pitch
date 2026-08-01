from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Enum, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin
from project.utils.enum import PositionCategoryEnum

if TYPE_CHECKING:
    from project.models.employee import Employee
    from project.models.employee_position import EmployeePosition
    from project.models.school import School


class Position(SchoolScopedMixin, BaseModel):
    __tablename__ = "positions"

    title: Mapped[str] = mapped_column(String(120), nullable=False)
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
    salary_grade: Mapped[Optional[str]] = mapped_column(
        String(30),
        nullable=True,
        default=None,
    )

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_position_id_school_id"),
        UniqueConstraint("school_id", "title", name="uq_position_school_title"),
    )

    school: Mapped[Optional["School"]] = relationship(
        "School",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    employee_positions: Mapped[List["EmployeePosition"]] = relationship(
        "EmployeePosition",
        back_populates="position",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="employee,employee_positions,school",
    )
    primary_for_employees: Mapped[List["Employee"]] = relationship(
        "Employee",
        foreign_keys="Employee.primary_position_id",
        back_populates="primary_position",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
