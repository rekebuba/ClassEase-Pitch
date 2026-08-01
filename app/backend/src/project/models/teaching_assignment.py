import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    UUID,
    ForeignKeyConstraint,
    UniqueConstraint,
)
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.base.school_mixin import SchoolScopedMixin

if TYPE_CHECKING:
    from project.models.class_section import ClassSection
    from project.models.school import School
    from project.models.subject import Subject
    from project.models.subject_offering import SubjectOffering
    from project.models.subject_term_result import SubjectTermResult
    from project.models.teacher_profile import TeacherProfile
    from project.models.year import Year


class TeachingAssignment(SchoolScopedMixin, BaseModel):
    __tablename__ = "teaching_assignments"

    teacher_profile_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    subject_offering_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    class_section_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False)
    # weekly_periods: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint(
            "id",
            "school_id",
            name="uq_teaching_assignment_id_school_id",
        ),
        UniqueConstraint(
            "school_id",
            "teacher_profile_id",
            "subject_offering_id",
            "class_section_id",
            name="uq_teaching_assignment_scope",
        ),
        ForeignKeyConstraint(
            ["teacher_profile_id", "school_id"],
            ["teacher_profiles.id", "teacher_profiles.school_id"],
            name="fk_teaching_assignment_profile_school",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["subject_offering_id", "school_id"],
            ["subject_offerings.id", "subject_offerings.school_id"],
            name="fk_teaching_assignment_subject_offering_school",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["class_section_id", "school_id"],
            ["class_sections.id", "class_sections.school_id"],
            name="fk_teaching_assignment_class_section_school",
            ondelete="CASCADE",
        ),
    )

    school: Mapped[Optional["School"]] = relationship(
        "School",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="teaching_assignments",
    )
    teacher_profile: Mapped["TeacherProfile"] = relationship(
        "TeacherProfile",
        back_populates="teaching_assignments",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="school,teaching_assignments",
    )
    subject_offering: Mapped["SubjectOffering"] = relationship(
        "SubjectOffering",
        back_populates="teaching_assignments",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="school,teacher_profile,teaching_assignments",
    )
    class_section: Mapped["ClassSection"] = relationship(
        "ClassSection",
        back_populates="teaching_assignments",
        init=False,
        repr=False,
        passive_deletes=True,
        overlaps="school,subject,teacher_profile,teaching_assignments,subject_offering",
    )
    subject_term_results: Mapped[List["SubjectTermResult"]] = relationship(
        "SubjectTermResult",
        back_populates="teaching_assignment",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="teaching_assignment,subject_offering,teacher_profile,class_section,student_term_record,subject_results,subject_term_results",
    )
    subject: AssociationProxy["Subject"] = association_proxy(
        "subject_offering",
        "subject",
        default=None,
    )
    subject_id: AssociationProxy[uuid.UUID] = association_proxy(
        "subject_offering",
        "subject_id",
        default=None,
    )
    academic_year: AssociationProxy["Year"] = association_proxy(
        "subject_offering",
        "year",
        default=None,
    )
    academic_year_id: AssociationProxy[uuid.UUID] = association_proxy(
        "subject_offering",
        "year_id",
        default=None,
    )
