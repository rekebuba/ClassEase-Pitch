import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import UUID, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.utils.enum import AuthSessionAssuranceEnum

if TYPE_CHECKING:
    from project.models.audit_log import AuditLog
    from project.models.school import School
    from project.models.school_membership import SchoolMembership
    from project.models.user import User


class AuthSession(BaseModel):
    __tablename__ = "auth_sessions"

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
    membership_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("school_memberships.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    refresh_token_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)
    ip_address: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True, default=None
    )
    assurance_level: Mapped[AuthSessionAssuranceEnum] = mapped_column(
        Enum(
            AuthSessionAssuranceEnum,
            name="auth_session_assurance_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=AuthSessionAssuranceEnum.PASSWORD_ONLY,
    )
    revoked_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )
    revoke_reason: Mapped[Optional[str]] = mapped_column(
        String(120),
        nullable=True,
        default=None,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="auth_sessions",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    school: Mapped["School"] = relationship(
        "School",
        back_populates="auth_sessions",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    membership: Mapped["SchoolMembership"] = relationship(
        "SchoolMembership",
        back_populates="auth_sessions",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    audit_logs: Mapped[list["AuditLog"]] = relationship(
        "AuditLog",
        back_populates="auth_session",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
