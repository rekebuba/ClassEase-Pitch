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
        semester (int): The semester in which the assessment was taken. Cannot be null.
        year (str): The year in which the assessment was taken. Cannot be null.

    Methods:
        __init__(*args, **kwargs): Initializes the assessment record with the provided arguments.
    """
    __tablename__ = 'assessments'
    student_id = Column(String(120), ForeignKey('student.id'), nullable=False)
    grade_id = Column(String(120), ForeignKey('grades.id'), nullable=False)
    subject_id = Column(String(120), ForeignKey('subjects.id'), nullable=False)
    total = Column(Float, default=None)  # The sum score of the student for each assessment
    rank = Column(Integer, default=None)
    semester = Column(Integer, nullable=False)
    year = Column(String(10), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
