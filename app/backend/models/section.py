#!/usr/bin/python3
"""Module for Section class"""

from typing import TYPE_CHECKING, List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship, scoped_session, Session
from models.base_model import BaseModel

if TYPE_CHECKING:
    from models.student_semester_record import StudentSemesterRecord


def seed_section(session: scoped_session[Session]) -> None:
    """
    Seed function to create default sections.
    """
    # Check if the table is already populated
    if session.query(Section).count() > 0:
        return

    sections = ["A", "B", "C"]
    for section in sections:
        new_section = Section(section=section)
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
    student_semester_records: Mapped[List["StudentSemesterRecord"]] = relationship(
        "StudentSemesterRecord",
        back_populates="section",
        default_factory=list,
        repr=False,
    )
