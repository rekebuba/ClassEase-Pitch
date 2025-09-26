#!/usr/bin/python3
"""Module for TeacherRecord class"""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import UUID, ForeignKey, UniqueConstraint
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base.base_model import BaseModel

if TYPE_CHECKING:
    from models.academic_term import AcademicTerm
    from models.employee import Employee
    from models.grade import Grade
    from models.grade_stream_subject import GradeStreamSubject
    from models.section import Section
    from models.subject import Subject


class TeacherRecord(BaseModel):
    __tablename__ = "teacher_records"
    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
    )
    academic_term_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("academic_terms.id", ondelete="CASCADE"),
        nullable=False,
    )
    grade_stream_subject_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(),
        ForeignKey("grade_stream_subjects.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )

    __table_args__ = (
        UniqueConstraint(
            "employee_id",
            "academic_term_id",
            "grade_stream_subject_id",
            name="uq_teacher_record",
        ),
    )

    # Many-To-One Relationships
    teacher: Mapped["Employee"] = relationship(
        "Employee",
        back_populates="teacher_records",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    academic_term: Mapped["AcademicTerm"] = relationship(
        "AcademicTerm",
        back_populates="teacher_records",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    grade_stream_subject: Mapped["GradeStreamSubject"] = relationship(
        "GradeStreamSubject",
        back_populates="teacher_records",
        init=False,
        repr=False,
        passive_deletes=True,
    )
    # Many-to-many relationship with sections
    sections: Mapped[List["Section"]] = relationship(
        "Section",
        secondary="teacher_record_links",
        back_populates="teacher_records",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    grade: AssociationProxy["Grade"] = association_proxy(
        "grade_stream_subject",
        "grade",
        default=None,
    )

    subject: AssociationProxy["Subject"] = association_proxy(
        "grade_stream_subject",
        "subject",
        default=None,
    )
