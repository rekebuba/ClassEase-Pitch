#!/usr/bin/python3
""" Module for MarkList class """

from sqlalchemy import String, Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel


class MarkList(BaseModel):
    """
    MarkList Model

    This model represents a list of marks for students in various assessments. It includes details about the student, grade, section, subject, teacher's record, semester, year, type of assessment, percentage contribution to the final score, and the actual score obtained.

    Attributes:
        student_id (str): Foreign key referencing the student's ID.
        subject_id (str): Foreign key referencing the subject's ID.
        teachers_record_id (str, optional): Foreign key referencing the teacher's record ID. Can be null and defaults to None.
        type (str): The type of assessment (e.g., 'Test', 'Quiz', 'Assignment', 'Midterm', 'Final').
        percentage (float): The percentage of this assessment towards the final score.
        score (float, optional): The actual score of the student in this assessment.

    Methods:
        __init__(*args, **kwargs): Initializes the MarkList instance, setting up the score attribute.
    """
    __tablename__ = 'mark_lists'

    user_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('users.id'), nullable=False)
    subject_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('subjects.id'), nullable=False)
    # e.g., 'Test', 'Quiz', 'Assignment', 'Midterm', 'Final'
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    percentage = mapped_column(Integer, nullable=False)
    score = mapped_column(Float, nullable=True, default=None)
    semester_record_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('student_semester_records.id'), nullable=False)
    teachers_record_id: Mapped[str] = mapped_column(String(120), ForeignKey(
        'teachers_records.id', ondelete="SET NULL"), nullable=True, default=None)
