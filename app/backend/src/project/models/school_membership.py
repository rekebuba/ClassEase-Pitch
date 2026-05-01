import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    UUID,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.utils.enum import MfaStateEnum, SchoolMembershipStatusEnum

if TYPE_CHECKING:
    from project.models.admin import Admin
    from project.models.audit_log import AuditLog
    from project.models.auth_session import AuthSession
    from project.models.employee import Employee
    from project.models.membership_role import MembershipRole
    from project.models.parent import Parent
    from project.models.role import Role
    from project.models.school import School
    from project.models.student import Student
    from project.models.transfer_request import TransferRequest
    from project.models.user import User


class SchoolMembership(BaseModel):
    __tablename__ = "school_memberships"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default_factory=lambda: datetime.now(timezone.utc),
    )
    status: Mapped[SchoolMembershipStatusEnum] = mapped_column(
        Enum(
            SchoolMembershipStatusEnum,
            name="school_membership_status_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=SchoolMembershipStatusEnum.ACTIVE,
    )
    login_identifier: Mapped[Optional[str]] = mapped_column(
        String(120),
        nullable=True,
        default=None,
    )
    left_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )
    mfa_state: Mapped[MfaStateEnum] = mapped_column(
        Enum(
            MfaStateEnum,
            name="mfa_state_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=MfaStateEnum.NOT_ENROLLED,
    )
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    permissions_version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="memberships",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    school: Mapped["School"] = relationship(
        "School",
        back_populates="memberships",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    membership_roles: Mapped[List["MembershipRole"]] = relationship(
        "MembershipRole",
        back_populates="membership",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    auth_sessions: Mapped[List["AuthSession"]] = relationship(
        "AuthSession",
        back_populates="membership",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    audit_logs: Mapped[List["AuditLog"]] = relationship(
        "AuditLog",
        back_populates="membership",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    admin_profiles: Mapped[List["Admin"]] = relationship(
        "Admin",
        back_populates="membership",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    employee_profiles: Mapped[List["Employee"]] = relationship(
        "Employee",
        back_populates="membership",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    student_profiles: Mapped[List["Student"]] = relationship(
        "Student",
        back_populates="membership",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    parent_profiles: Mapped[List["Parent"]] = relationship(
        "Parent",
        back_populates="membership",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    initiated_transfers: Mapped[List["TransferRequest"]] = relationship(
        "TransferRequest",
        foreign_keys="TransferRequest.requested_by_membership_id",
        back_populates="requested_by_membership",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    reviewed_transfers: Mapped[List["TransferRequest"]] = relationship(
        "TransferRequest",
        foreign_keys="TransferRequest.reviewed_by_membership_id",
        back_populates="reviewed_by_membership",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    @property
    def roles(self) -> List["Role"]:
        return [membership_role.role for membership_role in self.membership_roles]

    __table_args__ = (
        UniqueConstraint("user_id", "school_id", name="uq_membership_user_school"),
        UniqueConstraint(
            "school_id",
            "login_identifier",
            name="uq_membership_school_login_identifier",
        ),
    )
