from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Enum, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.utils.enum import RoleEnum

if TYPE_CHECKING:
    from project.models.membership_role import MembershipRole
    from project.models.role_permission import RolePermission


class Role(BaseModel):
    __tablename__ = "roles"

    name: Mapped[RoleEnum] = mapped_column(
        Enum(
            RoleEnum,
            name="roll_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)
    is_system: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    __table_args__ = (UniqueConstraint("name", name="uq_role_name"),)

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
