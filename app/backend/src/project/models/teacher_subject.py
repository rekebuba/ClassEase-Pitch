import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import UUID, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin

if TYPE_CHECKING:
    from project.models.school import School
    from project.models.subject import Subject
    from project.models.teacher_profile import TeacherProfile
    from project.models.year import Year


class TeacherSubject(SchoolScopedMixin, BaseModel):
    __tablename__ = "teacher_subjects"

    teacher_profile_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    subject_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    academic_year_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)

    __table_args__ = (
        UniqueConstraint("id", "school_id", name="uq_teacher_subject_id_school_id"),
        UniqueConstraint(
            "school_id",
            "teacher_profile_id",
            "subject_id",
            "academic_year_id",
            name="uq_teacher_subject_scope",
        ),
        ForeignKeyConstraint(
            ["teacher_profile_id", "school_id"],
            ["teacher_profiles.id", "teacher_profiles.school_id"],
            name="fk_teacher_subject_profile_school",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["subject_id", "school_id"],
            ["subjects.id", "subjects.school_id"],
            name="fk_teacher_subject_subject_school",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["academic_year_id", "school_id"],
            ["years.id", "years.school_id"],
            name="fk_teacher_subject_year_school",
            ondelete="CASCADE",
        ),
    )

    school: Mapped[Optional["School"]] = relationship(
        "School",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="teacher_subjects",
    )
    teacher_profile: Mapped["TeacherProfile"] = relationship(
        "TeacherProfile",
        back_populates="teacher_subjects",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="school,teacher_subjects",
    )
    subject: Mapped["Subject"] = relationship(
        "Subject",
        back_populates="teacher_subjects",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="school,teacher_profile,teacher_subjects",
    )
    academic_year: Mapped["Year"] = relationship(
        "Year",
        back_populates="teacher_subjects",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="school,subject,teacher_profile,teacher_subjects",
    )
