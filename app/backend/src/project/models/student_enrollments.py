import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    UUID,
    ForeignKeyConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin

if TYPE_CHECKING:
    from project.models.class_section import ClassSection
    from project.models.school import School
    from project.models.student import Student
    from project.models.student_term_record import StudentTermRecord
    from project.models.student_year_record import StudentYearRecord
    from project.models.year import Year


class StudentEnrollment(SchoolScopedMixin, BaseModel):
    __tablename__ = "student_enrollments"

    student_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    year_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    class_section_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "id",
            "school_id",
            name="uq_student_enrollment_id_school_id",
        ),
        UniqueConstraint(
            "school_id",
            "student_id",
            "year_id",
            name="uq_student_single_enrollment_per_year",
        ),
        ForeignKeyConstraint(
            ["student_id", "school_id"],
            ["students.id", "students.school_id"],
            name="fk_student_enrollment_profile_school",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["year_id", "school_id"],
            ["years.id", "years.school_id"],
            name="fk_student_enrollment_year_school",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["class_section_id", "school_id"],
            ["class_sections.id", "class_sections.school_id"],
            name="fk_student_enrollment_class_section_school",
            ondelete="CASCADE",
        ),
    )

    school: Mapped[Optional["School"]] = relationship(
        "School",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="student_enrollments",
    )
    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="student_enrollments",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="school,student_enrollments",
    )
    academic_year: Mapped["Year"] = relationship(
        "Year",
        back_populates="student_enrollments",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="school,student,student_enrollments",
    )
    class_section: Mapped["ClassSection"] = relationship(
        "ClassSection",
        back_populates="student_enrollments",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="academic_year,school,student,student_enrollments",
    )
    term_records: Mapped[List["StudentTermRecord"]] = relationship(
        "StudentTermRecord",
        back_populates="student_enrollment",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="student_enrollment,school,student,term_records,student_term_records",
    )
    student_year_record: Mapped[List["StudentYearRecord"]] = relationship(
        "StudentYearRecord",
        back_populates="student_enrollment",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="student_enrollment,school,student,student_year_record",
    )
