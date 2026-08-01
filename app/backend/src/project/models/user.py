#!/usr/bin/python3
"""Module for User class"""

from datetime import date
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Date, Enum, String, and_, true
from sqlalchemy.orm import Mapped, foreign, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.school_membership import SchoolMembership
from project.utils.enum import GenderEnum

if TYPE_CHECKING:
    from project.models.auth_identity import AuthIdentity
    from project.models.auth_session import AuthSession
    from project.models.saved_query_view import SavedQueryView


class User(BaseModel):
    """
    This module defines the User model which represents
    a user in the system. The User can have one of three
    roles: 'admin', 'teacher', or 'student'.
    Each user has a unique ID and a password.
    """

    __tablename__ = "users"
    # Common Profile Information
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    father_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    grand_father_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    gender: Mapped[Optional[GenderEnum]] = mapped_column(
        Enum(
            GenderEnum,
            name="gender_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=True,
    )
    email: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    username: Mapped[Optional[str]] = mapped_column(
        String(120),
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
    primary_membership: Mapped[Optional["SchoolMembership"]] = relationship(
        "SchoolMembership",
        primaryjoin=lambda: and_(
            User.id == foreign(SchoolMembership.user_id),
            SchoolMembership.is_primary == true(),
        ),
        uselist=False,
        viewonly=True,
        default=None,
        init=False,
    )
    memberships: Mapped[List["SchoolMembership"]] = relationship(
        "SchoolMembership",
        back_populates="user",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    auth_sessions: Mapped[List["AuthSession"]] = relationship(
        "AuthSession",
        back_populates="user",
        default_factory=list,
        init=False,
        passive_deletes=True,
    )

    """
    Note: If you use viewonly=True, you won't be able to do
    `user.children.append(another_user)`. you would have to use
    `parent.students.append(student)` instead.
    """
    children: Mapped[List["User"]] = relationship(
        "User",
        secondary="parent_student_links",
        primaryjoin="User.id == ParentStudentLink.parent_user_id",
        secondaryjoin="User.id == ParentStudentLink.student_user_id",
        back_populates="parents",
        viewonly=True,
        default_factory=list,
    )
    parents: Mapped[List["User"]] = relationship(
        "User",
        secondary="parent_student_links",
        primaryjoin="User.id == ParentStudentLink.student_user_id",
        secondaryjoin="User.id == ParentStudentLink.parent_user_id",
        back_populates="children",
        viewonly=True,
        default_factory=list,
    )
