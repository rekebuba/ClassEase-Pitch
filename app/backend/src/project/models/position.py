import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import UUID, Enum, ForeignKeyConstraint, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin
from project.utils.enum import PositionCategoryEnum

if TYPE_CHECKING:
    from project.models.department import Department
    from project.models.employee_position import EmployeePosition
    from project.models.school import School


class Position(SchoolScopedMixin, BaseModel):
    __tablename__ = "positions"

    title: Mapped[str] = mapped_column(String(120), nullable=False)
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(),
        nullable=True,
        default=None,
    )
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
        ForeignKeyConstraint(
            ["department_id", "school_id"],
            ["departments.id", "departments.school_id"],
            name="fk_position_department_school",
            ondelete="SET NULL",
        ),
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
    department: Mapped[Optional["Department"]] = relationship(
        "Department",
        foreign_keys=[department_id],
        back_populates="employees",
        init=False,
        repr=False,
        passive_deletes=True,
    )
