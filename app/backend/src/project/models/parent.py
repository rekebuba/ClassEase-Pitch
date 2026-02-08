#!/usr/bin/python3
"""Module for Parent class"""

from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.utils.enum import GenderEnum

if TYPE_CHECKING:
    from project.models.student import Student
    from project.models.user import User


class Parent(BaseModel):
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
    user_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        default=None,
    )

    # One-To-One Relationship
    user: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="parent",
        uselist=False,
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
