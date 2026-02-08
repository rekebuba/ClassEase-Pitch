#!/usr/bin/python3
"""Module for Admin class"""

import uuid
from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import UUID, Date, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.utils.enum import GenderEnum

if TYPE_CHECKING:
    from project.models.user import User


class Admin(BaseModel):
    """
    This model represents an admin in the system. It inherits from BaseModel and Base.
    """

    __tablename__ = "admins"
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    father_name: Mapped[str] = mapped_column(String(50), nullable=False)
    grand_father_name: Mapped[str] = mapped_column(String(50), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[GenderEnum] = mapped_column(
        Enum(
            GenderEnum,
            name="gender_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        default=None,
    )

    # One-to-One Relationship
    user: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="admin",
        init=False,
        repr=False,
        passive_deletes=True,
    )
