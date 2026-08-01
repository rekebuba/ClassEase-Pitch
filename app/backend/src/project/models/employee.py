import uuid
from datetime import date
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    UUID,
    CheckConstraint,
    Date,
    Enum,
    ForeignKeyConstraint,
    Index,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin
from project.utils.enum import EmploymentStatusEnum, EmploymentTypeEnum

if TYPE_CHECKING:
    from project.models.class_section import ClassSection
    from project.models.department import Department
    from project.models.employee_position import EmployeePosition
    from project.models.employment_contract import EmploymentContract
    from project.models.payroll_entry import PayrollEntry
    from project.models.payroll_profile import PayrollProfile
    from project.models.payroll_run import PayrollRun
    from project.models.position import Position
    from project.models.school import School
    from project.models.school_membership import SchoolMembership
    from project.models.teacher_profile import TeacherProfile


class Employee(SchoolScopedMixin, BaseModel):
    __tablename__ = "employees"

    employee_number: Mapped[str] = mapped_column(String(50), nullable=False)
    hire_date: Mapped[date] = mapped_column(Date, nullable=False)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(),
        nullable=True,
        default=None,
    )
    employment_status: Mapped[EmploymentStatusEnum] = mapped_column(
        Enum(
            EmploymentStatusEnum,
            name="employment_status_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=EmploymentStatusEnum.ACTIVE,
    )
    employment_type: Mapped[EmploymentTypeEnum] = mapped_column(
        Enum(
            EmploymentTypeEnum,
            name="employment_type_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=EmploymentTypeEnum.FULL_TIME,
    )
    termination_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        default=None,
    )
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(),
        nullable=True,
        default=None,
    )
    primary_position_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(),
        nullable=True,
        default=None,
    )
    manager_employee_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(),
        nullable=True,
        default=None,
    )
    work_email: Mapped[Optional[str]] = mapped_column(
        String(120),
        nullable=True,
        default=None,
    )
    work_phone: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        default=None,
    )

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_employee_id_school_id"),
        UniqueConstraint(
            "school_id",
            "employee_number",
            name="uq_employee_school_employee_number",
        ),
        CheckConstraint(
            "termination_date IS NULL OR termination_date >= hire_date",
            name="check_employee_dates",
        ),
        CheckConstraint(
            "manager_employee_id IS NULL OR manager_employee_id <> id",
            name="check_employee_not_self_manager",
        ),
        ForeignKeyConstraint(
            ["user_id", "school_id"],
            ["school_memberships.user_id", "school_memberships.school_id"],
            name="fk_employees_membership_school",
        ),
        ForeignKeyConstraint(
            ["department_id", "school_id"],
            ["departments.id", "departments.school_id"],
            name="fk_employee_department_school",
            ondelete="SET NULL",
        ),
        ForeignKeyConstraint(
            ["primary_position_id", "school_id"],
            ["positions.id", "positions.school_id"],
            name="fk_employee_primary_position_school",
            ondelete="SET NULL",
        ),
        ForeignKeyConstraint(
            ["manager_employee_id", "school_id"],
            ["employees.id", "employees.school_id"],
            name="fk_employee_manager_school",
            ondelete="SET NULL",
        ),
        Index(
            "uq_employee_school_user_when_present",
            "school_id",
            "user_id",
            unique=True,
            postgresql_where=text("user_id IS NOT NULL"),
        ),
    )

    membership: Mapped[Optional["SchoolMembership"]] = relationship(
        "SchoolMembership",
        back_populates="employee_profiles",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    school: Mapped[Optional["School"]] = relationship(
        "School",
        back_populates="employees",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="membership",
    )
    department: Mapped[Optional["Department"]] = relationship(
        "Department",
        foreign_keys=[department_id],
        back_populates="employees",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    primary_position: Mapped[Optional["Position"]] = relationship(
        "Position",
        foreign_keys=[primary_position_id],
        back_populates="primary_for_employees",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    manager: Mapped[Optional["Employee"]] = relationship(
        "Employee",
        foreign_keys=[manager_employee_id],
        remote_side="Employee.id",
        back_populates="direct_reports",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    direct_reports: Mapped[List["Employee"]] = relationship(
        "Employee",
        foreign_keys=[manager_employee_id],
        back_populates="manager",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    employee_positions: Mapped[List["EmployeePosition"]] = relationship(
        "EmployeePosition",
        back_populates="employee",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    teacher_profile: Mapped[Optional["TeacherProfile"]] = relationship(
        "TeacherProfile",
        back_populates="employee",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    payroll_profile: Mapped[Optional["PayrollProfile"]] = relationship(
        "PayrollProfile",
        back_populates="employee",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    payroll_entries: Mapped[List["PayrollEntry"]] = relationship(
        "PayrollEntry",
        back_populates="employee",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    processed_payroll_runs: Mapped[List["PayrollRun"]] = relationship(
        "PayrollRun",
        foreign_keys="PayrollRun.processed_by",
        back_populates="processor",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    employment_contracts: Mapped[List["EmploymentContract"]] = relationship(
        "EmploymentContract",
        back_populates="employee",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    headed_departments: Mapped[List["Department"]] = relationship(
        "Department",
        foreign_keys="Department.head_employee_id",
        back_populates="head_employee",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    homeroom_for_sections: Mapped[List["ClassSection"]] = relationship(
        "ClassSection",
        secondary="teacher_profiles",
        primaryjoin="Employee.id == TeacherProfile.employee_id",
        secondaryjoin="TeacherProfile.id == ClassSection.homeroom_teacher_id",
        viewonly=True,
        default_factory=list,
        repr=False,
    )
