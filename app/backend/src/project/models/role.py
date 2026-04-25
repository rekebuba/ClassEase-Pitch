import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import UUID, Boolean, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel

if TYPE_CHECKING:
    from project.models.membership_role import MembershipRole
    from project.models.role_permission import RolePermission
    from project.models.school import School


class Role(BaseModel):
    __tablename__ = "roles"

    school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, default=None
    )
    is_system: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    school: Mapped["School"] = relationship(
        "School",
        back_populates="roles",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    membership_roles: Mapped[List["MembershipRole"]] = relationship(
        "MembershipRole",
        back_populates="role",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    role_permissions: Mapped[List["RolePermission"]] = relationship(
        "RolePermission",
        back_populates="role",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    __table_args__ = (
        UniqueConstraint("school_id", "name", name="uq_role_school_name"),
    )
