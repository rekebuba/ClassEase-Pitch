import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import UUID, ForeignKeyConstraint, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin

if TYPE_CHECKING:
    from project.models.employee import Employee
    from project.models.school import School


class Department(SchoolScopedMixin, BaseModel):
    __tablename__ = "departments"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(30), nullable=False)
    head_employee_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(),
        nullable=True,
        default=None,
    )

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_department_id_school_id"),
        UniqueConstraint("school_id", "name", name="uq_department_school_name"),
        UniqueConstraint("school_id", "code", name="uq_department_school_code"),
        ForeignKeyConstraint(
            ["head_employee_id", "school_id"],
            ["employees.id", "employees.school_id"],
            name="fk_department_head_employee_school",
            ondelete="SET NULL",
        ),
    )

    school: Mapped[Optional["School"]] = relationship(
        "School",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    head_employee: Mapped[Optional["Employee"]] = relationship(
        "Employee",
        foreign_keys=[head_employee_id],
        back_populates="headed_departments",
        init=False,
        repr=False,
        passive_deletes=True,
    )
