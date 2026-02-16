#!/usr/bin/python3
"""Module for User class"""

from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Optional

from project.models.base.base_model import BaseModel
from project.utils.enum import RoleEnum

if TYPE_CHECKING:
    from project.models.admin import Admin
    from project.models.auth_identity import AuthIdentity
    from project.models.employee import Employee
    from project.models.parent import Parent
    from project.models.saved_query_view import SavedQueryView
    from project.models.student import Student


class User(BaseModel):
    """
    This module defines the User model which represents
    a user in the system. The User can have one of three
    roles: 'admin', 'teacher', or 'student'.
    Each user has a unique ID and a password.
    """

    __tablename__ = "users"
    role: Mapped[RoleEnum] = mapped_column(
        Enum(
            RoleEnum,
            name="role_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )
    email: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    username: Mapped[Optional[str]] = mapped_column(
        String(120),
        unique=True,
        nullable=True,
        default=None,
    )
    image_path: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        default=None,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    # One-to-One relationship
    admin: Mapped["Admin"] = relationship(
        "Admin",
        back_populates="user",
        uselist=False,
        init=False,
        repr=False,
        passive_deletes=True,
    )
    employee: Mapped["Employee"] = relationship(
        "Employee",
        back_populates="user",
        uselist=False,
        init=False,
        repr=False,
        passive_deletes=True,
    )
    parent: Mapped["Parent"] = relationship(
        "Parent",
        back_populates="user",
        uselist=False,
        init=False,
        repr=False,
        passive_deletes=True,
    )
    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="user",
        uselist=False,
        init=False,
        repr=False,
        passive_deletes=True,
    )
    saved_query_views: Mapped["SavedQueryView"] = relationship(
        "SavedQueryView",
        back_populates="user",
        cascade="all, delete-orphan",
        init=False,
        repr=False,
        passive_deletes=True,
    )

    auth_identities: Mapped[List["AuthIdentity"]] = relationship(
        "AuthIdentity",
        back_populates="user",
        default_factory=list,
        cascade="all, delete-orphan",
        repr=False,
        passive_deletes=True,
    )
