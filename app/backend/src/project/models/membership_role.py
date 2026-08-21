import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin

if TYPE_CHECKING:
    from project.models.role import Role
    from project.models.school_membership import SchoolMembership


class MembershipRole(SchoolScopedMixin, BaseModel):
    __tablename__ = "membership_roles"

    membership_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        nullable=False,
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("roles.id"),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("membership_id", "role_id", name="uq_membership_role"),
        ForeignKeyConstraint(
            ["membership_id", "school_id"],
            ["school_memberships.id", "school_memberships.school_id"],
            name="fk_membership_role_membership_school",
        ),
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
