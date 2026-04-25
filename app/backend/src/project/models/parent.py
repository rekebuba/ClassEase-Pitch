#!/usr/bin/python3
"""Module for Parent class"""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import UUID, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin
from project.utils.enum import GenderEnum

if TYPE_CHECKING:
    from project.models.school import School
    from project.models.school_membership import SchoolMembership
    from project.models.student import Student
    from project.models.user import User


class Parent(SchoolScopedMixin, BaseModel):
    """
    Represents a parent entity in the database.
    """

    __tablename__ = "parents"

    # Personal Information
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[GenderEnum] = mapped_column(
        Enum(
            GenderEnum,
            name="gender_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(String(120), nullable=True, unique=True)
    phone: Mapped[str] = mapped_column(String(25), nullable=False)
    relation: Mapped[str] = mapped_column(String(50), nullable=False)

    emergency_contact_phone: Mapped[Optional[str]] = mapped_column(
        String(25),
        nullable=True,
        default=None,
    )
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(),
        ForeignKey("users.id"),
        nullable=True,
        default=None,
    )
    school_membership_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(),
        ForeignKey("school_memberships.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )

    # Relationships
    user: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="parent_profiles",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    membership: Mapped[Optional["SchoolMembership"]] = relationship(
        "SchoolMembership",
        back_populates="parent_profiles",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    school: Mapped[Optional["School"]] = relationship(
        "School",
        back_populates="parents",
        init=False,
        repr=False,
        passive_deletes=True,
    )

    # Many-To-Many Relationships
    students: Mapped[List["Student"]] = relationship(
        "Student",
        secondary="parent_student_links",
        back_populates="parents",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
