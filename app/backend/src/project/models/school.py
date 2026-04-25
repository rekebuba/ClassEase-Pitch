from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlalchemy import JSON, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.utils.enum import SchoolStatusEnum

if TYPE_CHECKING:
    from project.models.admin import Admin
    from project.models.audit_log import AuditLog
    from project.models.auth_session import AuthSession
    from project.models.employee import Employee
    from project.models.parent import Parent
    from project.models.role import Role
    from project.models.school_membership import SchoolMembership
    from project.models.student import Student
    from project.models.transfer_request import TransferRequest
    from project.models.year import Year


class School(BaseModel):
    __tablename__ = "schools"

    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    status: Mapped[SchoolStatusEnum] = mapped_column(
        Enum(
            SchoolStatusEnum,
            name="school_status_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=SchoolStatusEnum.ACTIVE,
    )
    domain: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, default=None
    )
    logo_path: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, default=None
    )
    primary_color: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True, default=None
    )
    settings: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
        default_factory=dict,
    )

    memberships: Mapped[List["SchoolMembership"]] = relationship(
        "SchoolMembership",
        back_populates="school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    roles: Mapped[List["Role"]] = relationship(
        "Role",
        back_populates="school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    years: Mapped[List["Year"]] = relationship(
        "Year",
        back_populates="school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    admins: Mapped[List["Admin"]] = relationship(
        "Admin",
        back_populates="school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    employees: Mapped[List["Employee"]] = relationship(
        "Employee",
        back_populates="school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    students: Mapped[List["Student"]] = relationship(
        "Student",
        back_populates="school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    parents: Mapped[List["Parent"]] = relationship(
        "Parent",
        back_populates="school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    auth_sessions: Mapped[List["AuthSession"]] = relationship(
        "AuthSession",
        back_populates="school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    audit_logs: Mapped[List["AuditLog"]] = relationship(
        "AuditLog",
        back_populates="school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    initiated_transfers: Mapped[List["TransferRequest"]] = relationship(
        "TransferRequest",
        foreign_keys="TransferRequest.source_school_id",
        back_populates="source_school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    received_transfers: Mapped[List["TransferRequest"]] = relationship(
        "TransferRequest",
        foreign_keys="TransferRequest.target_school_id",
        back_populates="target_school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
