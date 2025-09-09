#!/usr/bin/python3
"""Module for User class"""

from typing import TYPE_CHECKING
from sqlalchemy import Boolean, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extension.enums.enum import RoleEnum
from models.base.base_model import BaseModel

if TYPE_CHECKING:
    from models.admin import Admin
    from models.student import Student
    from models.teacher import Teacher
    from models.saved_query_view import SavedQueryView


class User(BaseModel):
    """
    This module defines the User model which represents a user in the system. The User can have one of three roles: 'admin', 'teacher', or 'student'. Each user has a unique ID and a password.
    """

    __tablename__ = "users"
    identification: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[RoleEnum] = mapped_column(
        Enum(
            RoleEnum,
            name="role_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )
    image_path: Mapped[str] = mapped_column(String(255), nullable=True, default=None)
    # is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # One-to-many relationship
    admin: Mapped["Admin"] = relationship(
        "Admin",
        back_populates="user",
        uselist=False,
        init=False,
        repr=False,
        passive_deletes=True,
    )
    teacher: Mapped["Teacher"] = relationship(
        "Teacher",
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
