#!/usr/bin/python3
""" Module for TeachersRecord class """

from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel


class TeachersRecord(BaseModel):
    """
    TeachersRecord Model

    This model represents the record of teachers, including their associated subjects, grades, and sections.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        teacher_id (str): Foreign key referencing the teacher's ID.
        subject_id (str): Foreign key referencing the subject's ID. Nullable.
        grade_id (str): Foreign key referencing the grade's ID. Nullable.
        section_id (str): Foreign key referencing the section's ID. Nullable.
        mark_list (relationship): Relationship to the MarkList model with cascade save-update and passive deletes.

    Methods:
        __init__(*args, **kwargs): Initializes a TeachersRecord instance.
    """
    __tablename__ = 'teachers_records'
    user_id: Mapped[str] = mapped_column(String(120), ForeignKey(
        'users.id'), nullable=False)
    semester_id: Mapped[str] = mapped_column(String(120), ForeignKey(
        'semesters.id'), nullable=False)
    subject_id: Mapped[str] = mapped_column(String(120), ForeignKey(
        'subjects.id'), nullable=True, default=None)
    grade_id: Mapped[str] = mapped_column(String(120), ForeignKey(
        'grades.id'), nullable=True, default=None)
    section_id: Mapped[str] = mapped_column(String(120), ForeignKey(
        'sections.id'), nullable=True, default=None)

    mark_list = relationship(
        "MarkList", backref="teachers_record", cascade="save-update", passive_deletes=True)
    assessment = relationship(
        "Assessment", backref="teachers_record", cascade="save-update", passive_deletes=True)

    def __init__(self, *args, **kwargs):
        """
        Initializes the score.

        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
