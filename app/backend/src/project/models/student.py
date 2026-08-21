#!/usr/bin/python3
"""Module for Student class"""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    UUID,
    Enum,
    ForeignKeyConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin
from project.utils.enum import StudentApplicationStatusEnum

if TYPE_CHECKING:
    from project.models.school import School
    from project.models.school_membership import SchoolMembership
    from project.models.student_academic_background import StudentAcademicBackground
    from project.models.student_address import StudentAddress
    from project.models.student_enrollments import StudentEnrollment
    from project.models.student_health_record import StudentHealthRecord


class Student(SchoolScopedMixin, BaseModel):
    """
    Represents a student entity in the database.
    """

    __tablename__ = "students"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
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

    health_record: Mapped["StudentHealthRecord"] = relationship(
        "StudentHealthRecord",
        back_populates="student",
        init=False,
        uselist=False,
    )
    academic_background: Mapped["StudentAcademicBackground"] = relationship(
        "StudentAcademicBackground",
        back_populates="student",
        init=False,
        uselist=False,
    )
    address: Mapped["StudentAddress"] = relationship(
        "StudentAddress",
        back_populates="student",
        init=False,
        uselist=False,
    )
