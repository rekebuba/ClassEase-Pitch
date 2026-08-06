import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    UUID,
    Enum,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin
from project.utils.enum import HighestEducationEnum

if TYPE_CHECKING:
    from project.models.class_section import ClassSection
    from project.models.employee import Employee
    from project.models.school import School
    from project.models.teacher_subject import TeacherSubject
    from project.models.teaching_assignment import TeachingAssignment


class TeacherProfile(SchoolScopedMixin, BaseModel):
    __tablename__ = "teacher_profiles"

    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    specialization: Mapped[Optional[str]] = mapped_column(
        String(120),
        nullable=True,
        default=None,
    )
    teacher_license_number: Mapped[Optional[str]] = mapped_column(
        String(80),
        nullable=True,
        default=None,
    )
    certifications: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        default=None,
    )
    highest_education: Mapped[Optional[HighestEducationEnum]] = mapped_column(
        Enum(
            HighestEducationEnum,
            name="teacher_highest_education_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=True,
        default=None,
    )
    years_of_experience: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        default=None,
    )

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_teacher_profile_id_school_id"),
        UniqueConstraint(
            "school_id",
            "employee_id",
            name="uq_teacher_profile_school_employee",
        ),
        ForeignKeyConstraint(
            ["employee_id", "school_id"],
            ["employees.id", "employees.school_id"],
            name="fk_teacher_profile_employee_school",
            ondelete="CASCADE",
        ),
        Index(
            "uq_teacher_profile_school_license_not_null",
            "school_id",
            "teacher_license_number",
            unique=True,
            postgresql_where=text("teacher_license_number IS NOT NULL"),
        ),
    )

    school: Mapped[Optional["School"]] = relationship(
        "School",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="teacher_profile,teacher_profiles",
    )
    employee: Mapped["Employee"] = relationship(
        "Employee",
        back_populates="teacher_profile",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="school,teacher_profiles",
    )
    teacher_subjects: Mapped[List["TeacherSubject"]] = relationship(
        "TeacherSubject",
        back_populates="teacher_profile",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="teacher_subjects",
    )
    teaching_assignments: Mapped[List["TeachingAssignment"]] = relationship(
        "TeachingAssignment",
        back_populates="teacher_profile",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="teaching_assignments",
    )
    homeroom_sections: Mapped[List["ClassSection"]] = relationship(
        "ClassSection",
        back_populates="homeroom_teacher",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="academic_year,class_sections,grade_stream,school,section",
    )
