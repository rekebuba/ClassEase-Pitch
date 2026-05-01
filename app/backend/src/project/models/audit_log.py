import uuid
from typing import TYPE_CHECKING, Any, Dict, Optional

from sqlalchemy import JSON, UUID, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel

if TYPE_CHECKING:
    from project.models.auth_session import AuthSession
    from project.models.school import School
    from project.models.school_membership import SchoolMembership
    from project.models.user import User


class AuditLog(BaseModel):
    __tablename__ = "audit_logs"

    school_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(),
        ForeignKey("schools.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    membership_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(),
        ForeignKey("school_memberships.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    auth_session_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(),
        ForeignKey("auth_sessions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    action: Mapped[str] = mapped_column(String(120), nullable=False)
    resource_type: Mapped[Optional[str]] = mapped_column(
        String(120),
        nullable=True,
        default=None,
    )
    resource_id: Mapped[Optional[str]] = mapped_column(
        String(120),
        nullable=True,
        default=None,
    )
    outcome: Mapped[str] = mapped_column(String(40), nullable=False, default="success")
    ip_address: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True, default=None
    )
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)
    details: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
        default_factory=dict,
    )

    school: Mapped[Optional["School"]] = relationship(
        "School",
        back_populates="audit_logs",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    user: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="audit_logs",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    membership: Mapped[Optional["SchoolMembership"]] = relationship(
        "SchoolMembership",
        back_populates="audit_logs",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    auth_session: Mapped[Optional["AuthSession"]] = relationship(
        "AuthSession",
        back_populates="audit_logs",
        init=False,
        repr=False,
        passive_deletes=True,
    )
