from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel

if TYPE_CHECKING:
    from project.models.role_permission import RolePermission


class Permission(BaseModel):
    __tablename__ = "permissions"

    code: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, default=None
    )

    role_permissions: Mapped[List["RolePermission"]] = relationship(
        "RolePermission",
        back_populates="permission",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
