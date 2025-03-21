#!/usr/bin/python3
""" Module for STUDYearRecord class """

from sqlalchemy import Integer, String, ForeignKey, CheckConstraint, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel


class STUDYearRecord(BaseModel):
    """
    Represents a student's yearly academic record.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        student_id (str): The ID of the student, foreign key referencing 'student.id'.
        year_id (str): The ID of the year, foreign key referencing 'years.id'.
        grade_id (str): The ID of the grade, foreign key referencing 'grades.id'.
        section_id (str): The ID of the section, foreign key referencing 'sections.id'.
        final_score (float): The final score for the year, default is None.
        rank (int): The rank of the student, default is None.

    Relationships:
        student (relationship): Relationship to the Student model (commented out).

    Methods:
        __init__(*args, **kwargs): Initializes the STUDYearRecord instance.
    """
    __tablename__ = 'student_year_records'
    user_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('users.id'), nullable=False)
    grade_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('grades.id'), nullable=False)
    year_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('years.id'), nullable=False)
    final_score: Mapped[float] = mapped_column(
        Float, nullable=True, default=None)  # year-end score
    rank: Mapped[int] = mapped_column(Integer, nullable=True, default=None)
