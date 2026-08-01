import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import UUID, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin

if TYPE_CHECKING:
    from project.models.school import School
    from project.models.section import Section
    from project.models.student_enrollments import StudentEnrollment
    from project.models.teacher_profile import TeacherProfile
    from project.models.teaching_assignment import TeachingAssignment
    from project.models.year import Year


class ClassSection(SchoolScopedMixin, BaseModel):
    __tablename__ = "class_sections"

    section_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    stream_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(), nullable=True)
    academic_year_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    homeroom_teacher_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(),
        nullable=True,
        default=None,
    )

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_class_section_id_school_id"),
        UniqueConstraint(
            "school_id",
            "section_id",
            "academic_year_id",
            name="uq_class_section_scope",
        ),
        ForeignKeyConstraint(
            ["section_id", "school_id"],
            ["sections.id", "sections.school_id"],
            name="fk_class_section_section_school",
            ondelete="SET NULL",
        ),
        ForeignKeyConstraint(
            ["stream_id", "school_id"],
            ["streams.id", "streams.school_id"],
            name="fk_class_section_stream_school",
            ondelete="SET NULL",
        ),
        ForeignKeyConstraint(
            ["academic_year_id", "school_id"],
            ["years.id", "years.school_id"],
            name="fk_class_section_year_school",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["homeroom_teacher_id", "school_id"],
            ["teacher_profiles.id", "teacher_profiles.school_id"],
            name="fk_class_section_homeroom_teacher_school",
            ondelete="SET NULL",
        ),
    )

    school: Mapped[Optional["School"]] = relationship(
        "School",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    section: Mapped["Section"] = relationship(
        "Section",
        back_populates="class_sections",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="school",
    )
    academic_year: Mapped["Year"] = relationship(
        "Year",
        back_populates="class_sections",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="section,school",
    )
    homeroom_teacher: Mapped[Optional["TeacherProfile"]] = relationship(
        "TeacherProfile",
        back_populates="homeroom_sections",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="academic_year,section,school",
    )
    teaching_assignments: Mapped[List["TeachingAssignment"]] = relationship(
        "TeachingAssignment",
        back_populates="class_section",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    student_enrollments: Mapped[List["StudentEnrollment"]] = relationship(
        "StudentEnrollment",
        back_populates="class_section",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="academic_year,school,student,student_enrollments",
    )
