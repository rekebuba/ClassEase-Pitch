import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel

if TYPE_CHECKING:
    from project.models.role import Role
    from project.models.school_membership import SchoolMembership


class MembershipRole(BaseModel):
    __tablename__ = "membership_roles"

    membership_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("school_memberships.id", ondelete="CASCADE"),
        nullable=False,
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
    )

    membership: Mapped["SchoolMembership"] = relationship(
        "SchoolMembership",
        back_populates="membership_roles",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="membership_roles",
        init=False,
        repr=False,
        passive_deletes=True,
    )

    __table_args__ = (
        UniqueConstraint("membership_id", "role_id", name="uq_membership_role"),
    )
