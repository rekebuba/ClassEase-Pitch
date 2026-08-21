#!/usr/bin/python3
"""Module for Year class"""

from datetime import date
from typing import TYPE_CHECKING, List

from sqlalchemy import CheckConstraint, Date, Enum, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin
from project.utils.enum import AcademicTermTypeEnum, AcademicYearStatusEnum

if TYPE_CHECKING:
    from project.models.academic_term import AcademicTerm
    from project.models.class_section import ClassSection
    from project.models.event import Event
    from project.models.school import School
    from project.models.student_enrollments import StudentEnrollment
    from project.models.subject_offering import SubjectOffering
    from project.models.teacher_subject import TeacherSubject


class Year(SchoolScopedMixin, BaseModel):
    """docstring for year."""

    __tablename__ = "years"

    calendar_type: Mapped[AcademicTermTypeEnum] = mapped_column(
        Enum(
            AcademicTermTypeEnum,
            name="term_type_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(
        Enum(
            AcademicYearStatusEnum,
            name="year_status_enum",
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
    )
    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_year_id_school_id"),
        UniqueConstraint("school_id", "name", name="uq_year_school_name"),
        CheckConstraint("start_date <= end_date", name="check_year_dates"),
    )

    # Relationships
    events: Mapped[List["Event"]] = relationship(
        "Event",
        back_populates="year",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    academic_terms: Mapped[List["AcademicTerm"]] = relationship(
        "AcademicTerm",
        back_populates="year",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    subject_offerings: Mapped[List["SubjectOffering"]] = relationship(
        "SubjectOffering",
        back_populates="year",
        repr=False,
        passive_deletes=True,
        default_factory=list,
        overlaps="subject_offerings",
    )
    class_sections: Mapped[List["ClassSection"]] = relationship(
        "ClassSection",
        back_populates="academic_year",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="class_sections,grade_stream,homeroom_teacher,school,section",
    )
    teacher_subjects: Mapped[List["TeacherSubject"]] = relationship(
        "TeacherSubject",
        back_populates="academic_year",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="teacher_subjects",
    )
    school: Mapped["School"] = relationship(
        "School",
        back_populates="years",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    student_enrollments: Mapped[List["StudentEnrollment"]] = relationship(
        "StudentEnrollment",
        back_populates="academic_year",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="student,school,student_enrollments",
    )
