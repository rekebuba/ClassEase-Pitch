#!/usr/bin/python3
""" Module for Assessment class """

from sqlalchemy import Column, String, Integer, ForeignKey, Float
from models.engine.db_storage import BaseModel, Base

class Assessment(BaseModel, Base):
    """
    Assessment Model

    This model represents an assessment record for a student, including details such as the student's ID, grade ID, subject ID, total score, rank, semester, and year.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        student_id (str): Foreign key referencing the student's ID.
        grade_id (str): Foreign key referencing the grade's ID.
        subject_id (str): Foreign key referencing the subject's ID.
        total (float): The sum score of the student for each assessment. Default is None.
        rank (int): The rank of the student in the assessment. Default is None.

    Methods:
        __init__(*args, **kwargs): Initializes the assessment record with the provided arguments.
    """
    __tablename__ = 'assessments'
    student_id = Column(String(120), ForeignKey('student.user_id'), nullable=False)
    grade_id = Column(String(120), ForeignKey('grades.id'), nullable=False)
    section_id = Column(String(120), ForeignKey('sections.id'), nullable=False)
    subject_id = Column(String(120), ForeignKey('subjects.id'), nullable=False)
    teachers_record_id = Column(String(120), ForeignKey('teachers_record.id', ondelete="SET NULL"), nullable=True, default=None)
    total = Column(Float, default=None)  # The subject sum score of the student for each assessment
    rank = Column(Integer, default=None)
    semester_id = Column(String(120), ForeignKey('semesters.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
