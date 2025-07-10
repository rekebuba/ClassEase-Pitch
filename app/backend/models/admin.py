#!/usr/bin/python3
"""Module for Admin class"""

from typing import TYPE_CHECKING, Optional
from sqlalchemy import Date, Enum, String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extension.enums.enum import GenderEnum
from models.base_model import BaseModel

if TYPE_CHECKING:
    from models.user import User


class Admin(BaseModel):
    """
    This model represents an admin in the system. It inherits from BaseModel and Base.
    """

    __tablename__ = "admins"
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    father_name: Mapped[str] = mapped_column(String(50), nullable=False)
    grand_father_name: Mapped[str] = mapped_column(String(50), nullable=False)
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    gender: Mapped[GenderEnum] = mapped_column(
        Enum(
            GenderEnum,
            name="gender_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(25), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id"),
        nullable=True,
        default=None,
    )

    user: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="admin",
        init=False,
        repr=False,
    )
