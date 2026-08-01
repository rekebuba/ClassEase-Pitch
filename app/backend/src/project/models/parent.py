#!/usr/bin/python3
"""Module for Parent class"""

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import UUID, ForeignKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin

if TYPE_CHECKING:
    from project.models.school import School
    from project.models.school_membership import SchoolMembership


class Parent(SchoolScopedMixin, BaseModel):
    """
    Represents a parent entity in the database.
    """

    __tablename__ = "parents"

    relation: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        nullable=True,
        default=None,
    )

    emergency_contact_phone: Mapped[Optional[str]] = mapped_column(
        String(25),
        nullable=True,
        default=None,
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id", "school_id"],
            [
                "school_memberships.user_id",
                "school_memberships.school_id",
            ],
            name="fk_parents_membership_school",
        ),
    )

    # Relationships
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
        overlaps="membership",
    )
