#!/usr/bin/python3
"""Module for User class"""

from typing import TYPE_CHECKING, Iterable, List, Optional

from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.core.tenant import get_current_school_id
from project.models.base.base_model import BaseModel
from project.utils.enum import RoleEnum

if TYPE_CHECKING:
    from project.models.admin import Admin
    from project.models.audit_log import AuditLog
    from project.models.auth_identity import AuthIdentity
    from project.models.auth_session import AuthSession
    from project.models.employee import Employee
    from project.models.parent import Parent
    from project.models.saved_query_view import SavedQueryView
    from project.models.school_membership import SchoolMembership
    from project.models.student import Student
    from project.models.transfer_request import TransferRequest


class User(BaseModel):
    """
    This module defines the User model which represents
    a user in the system. The User can have one of three
    roles: 'admin', 'teacher', or 'student'.
    Each user has a unique ID and a password.
    """

    __tablename__ = "users"
    role: Mapped[RoleEnum] = mapped_column(
        Enum(
            RoleEnum,
            name="role_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )
    email: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    username: Mapped[Optional[str]] = mapped_column(
        String(120),
        nullable=True,
        default=None,
    )
    image_path: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        default=None,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    admin_profiles: Mapped[List["Admin"]] = relationship(
        "Admin",
        back_populates="user",
        default_factory=list,
        init=False,
        repr=False,
        passive_deletes=True,
    )
    employee_profiles: Mapped[List["Employee"]] = relationship(
        "Employee",
        back_populates="user",
        default_factory=list,
        init=False,
        repr=False,
        passive_deletes=True,
    )
    parent_profiles: Mapped[List["Parent"]] = relationship(
        "Parent",
        back_populates="user",
        default_factory=list,
        init=False,
        repr=False,
        passive_deletes=True,
    )
    student_profiles: Mapped[List["Student"]] = relationship(
        "Student",
        back_populates="user",
        default_factory=list,
        init=False,
        repr=False,
        passive_deletes=True,
    )
    saved_query_views: Mapped["SavedQueryView"] = relationship(
        "SavedQueryView",
        back_populates="user",
        cascade="all, delete-orphan",
        init=False,
        repr=False,
        passive_deletes=True,
    )

    auth_identities: Mapped[List["AuthIdentity"]] = relationship(
        "AuthIdentity",
        back_populates="user",
        default_factory=list,
        cascade="all, delete-orphan",
        repr=False,
        passive_deletes=True,
    )
    memberships: Mapped[List["SchoolMembership"]] = relationship(
        "SchoolMembership",
        back_populates="user",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    auth_sessions: Mapped[List["AuthSession"]] = relationship(
        "AuthSession",
        back_populates="user",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    audit_logs: Mapped[List["AuditLog"]] = relationship(
        "AuditLog",
        back_populates="user",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    transfer_requests: Mapped[List["TransferRequest"]] = relationship(
        "TransferRequest",
        back_populates="subject_user",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    def _resolve_scoped_profile(self, profiles: Iterable[object]) -> object | None:
        school_id = get_current_school_id()
        profile_list = list(profiles)
        if school_id is not None:
            for profile in profile_list:
                if getattr(profile, "school_id", None) == school_id:
                    return profile
        return profile_list[0] if profile_list else None

    @property
    def admin(self) -> Optional["Admin"]:
        return self._resolve_scoped_profile(self.admin_profiles)  # type: ignore[return-value]

    @property
    def employee(self) -> Optional["Employee"]:
        return self._resolve_scoped_profile(self.employee_profiles)  # type: ignore[return-value]

    @property
    def teacher(self) -> Optional["Employee"]:
        return self.employee

    @property
    def parent(self) -> Optional["Parent"]:
        return self._resolve_scoped_profile(self.parent_profiles)  # type: ignore[return-value]

    @property
    def student(self) -> Optional["Student"]:
        return self._resolve_scoped_profile(self.student_profiles)  # type: ignore[return-value]
