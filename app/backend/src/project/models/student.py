#!/usr/bin/python3
"""Module for Student class"""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    UUID,
    Boolean,
    Enum,
    ForeignKeyConstraint,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin
from project.utils.enum import BloodTypeEnum, StudentApplicationStatusEnum

if TYPE_CHECKING:
    from project.models.school import School
    from project.models.school_membership import SchoolMembership
    from project.models.student_enrollments import StudentEnrollment


class Student(SchoolScopedMixin, BaseModel):
    """
    Represents a student entity in the database.
    """

    __tablename__ = "students"

    # Contact Information
    city: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, default=None)
    state: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, default=None)
    postal_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, default=None)

    nationality: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, default=None)
    blood_type: Mapped[BloodTypeEnum] = mapped_column(
        Enum(
            BloodTypeEnum,
            name="blood_type_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=True,
        default=BloodTypeEnum.UNKNOWN,
    )
    student_photo: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, default=None)
    previous_school: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, default=None)
    transportation: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, default=None)
    disability_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)
    medical_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)

    # Defaulted Fields
    has_medical_condition: Mapped[bool] = mapped_column(Boolean, default=False)
    has_disability: Mapped[bool] = mapped_column(Boolean, default=False)
    is_transfer: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[StudentApplicationStatusEnum] = mapped_column(
        Enum(
            StudentApplicationStatusEnum,
            name="student_application_status_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=StudentApplicationStatusEnum.PENDING,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        nullable=True,
        default=None,
    )

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_student_id_school_id"),
        ForeignKeyConstraint(
            ["user_id", "school_id"],
            [
                "school_memberships.user_id",
                "school_memberships.school_id",
            ],
            name="fk_students_membership_school",
        ),
    )

    # Relationships
    membership: Mapped[Optional["SchoolMembership"]] = relationship(
        "SchoolMembership",
        back_populates="student_profiles",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="students",
    )
    school: Mapped[Optional["School"]] = relationship(
        "School",
        back_populates="students",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="membership,student_profiles",
    )
    student_enrollments: Mapped[List["StudentEnrollment"]] = relationship(
        "StudentEnrollment",
        back_populates="student",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="student,school,student_enrollments",
    )
