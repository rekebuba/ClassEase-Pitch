#!/usr/bin/python3
"""Module for Section class"""

from typing import TYPE_CHECKING, List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship, scoped_session, Session
from extension.enums.enum import SectionEnum
from models.base_model import BaseModel

if TYPE_CHECKING:
    from models.student_term_record import StudentTermRecord
    from models.teacher_record import TeachersRecord
    from models.yearly_subject import YearlySubject


def seed_section(session: scoped_session[Session]) -> None:
    """
    Seed function to create default sections.
    """
    # Check if the table is already populated
    if session.query(Section).count() > 0:
        return

    for section_name in SectionEnum:
        new_section = Section(section=section_name.value)
        session.add(new_section)

    session.commit()


class Section(BaseModel):
    """
    Represents a section within a grade.
    """

    __tablename__ = "sections"
    section: Mapped[str] = mapped_column(
        String(1), nullable=True, default=None
    )  # e.g., A, B, C, D, E, F, G

    # Relationships
    student_term_records: Mapped[List["StudentTermRecord"]] = relationship(
        "StudentTermRecord",
        back_populates="section",
        default_factory=list,
        repr=False,
    )

    # Many-to-many relationships
    teacher_records_link: Mapped[List["TeachersRecord"]] = relationship(
        "TeachersRecord",
        back_populates="sections_link",
        secondary="teacher_record_section_links",
        default_factory=list,
        repr=False,
    )
    yearly_subjects_link: Mapped[List["YearlySubject"]] = relationship(
        "YearlySubject",
        back_populates="sections_link",
        secondary="yearly_subject_section_links",
        default_factory=list,
        repr=False,
    )
