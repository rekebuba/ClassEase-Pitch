import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import UUID, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.utils.enum import AuthProviderEnum

if TYPE_CHECKING:
    from project.models.user import User


class AuthIdentity(BaseModel):
    __tablename__ = "auth_identities"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    provider: Mapped[str] = mapped_column(
        Enum(
            AuthProviderEnum,
            name="auth_provider_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )
    provider_user_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
        default=None,
    )  # google_sub, github_id, etc
    password: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        default=None,
    )  # Only for provider="password"

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="auth_identities",
        init=False,
        repr=False,
        passive_deletes=True,
    )
