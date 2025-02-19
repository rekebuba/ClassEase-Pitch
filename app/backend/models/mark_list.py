#!/usr/bin/python3
""" Module for MarkList class """

from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from models.engine.db_storage import BaseModel, Base


class MarkList(BaseModel, Base):
    """
    MarkList Model

    This model represents a list of marks for students in various assessments. It includes details about the student, grade, section, subject, teacher's record, semester, year, type of assessment, percentage contribution to the final score, and the actual score obtained.

    Attributes:
        student_id (str): Foreign key referencing the student's ID.
        grade_id (str): Foreign key referencing the grade's ID.
        section_id (str): Foreign key referencing the section's ID.
        subject_id (str): Foreign key referencing the subject's ID.
        teachers_record_id (str, optional): Foreign key referencing the teacher's record ID. Can be null and defaults to None.
        semester (int): The semester in which the assessment was taken.
        year (str): The academic year in which the assessment was taken.
        type (str): The type of assessment (e.g., 'Test', 'Quiz', 'Assignment', 'Midterm', 'Final').
        percentage (float): The percentage of this assessment towards the final score.
        score (float, optional): The actual score of the student in this assessment.

    Methods:
        __init__(*args, **kwargs): Initializes the MarkList instance, setting up the score attribute.
    """
    __tablename__ = 'mark_lists'
    student_id = Column(String(120), ForeignKey('student.id'), nullable=False)
    grade_id = Column(String(120), ForeignKey('grades.id'), nullable=False)
    section_id = Column(String(120), ForeignKey('sections.id'))
    subject_id = Column(String(120), ForeignKey('subjects.id'), nullable=False)
    teachers_record_id = Column(String(120), ForeignKey('teachers_record.id', ondelete="SET NULL"), nullable=True, default=None)
    semester = Column(Integer, nullable=False)
    year = Column(String(10), nullable=False)
    type = Column(String(50), nullable=False)  # e.g., 'Test', 'Quiz', 'Assignment', 'Midterm', 'Final'
    percentage = Column(Float, nullable=False)  # percentage of this assessment towards the final score
    score = Column(Float)  # The actual score of the student in this assessment

    def __init__(self, *args, **kwargs):
        """
        Initializes the score.

        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
