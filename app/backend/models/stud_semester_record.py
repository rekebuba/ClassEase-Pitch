#!/usr/bin/python3
""" Module for Average Result class """

from sqlalchemy import String, Integer, ForeignKey, Float
from models.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

class STUDSemesterRecord(BaseModel):
    """
    STUDSemesterRecord Model

    This model represents the average result of a student for a particular semester and year.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        student_id (str): The ID of the student, which is a foreign key referencing the 'student' table.
        average (float): The average score of the student in the assessment. Default is None.
        semester_id (Str): The semester for which the average result is recorded.
        year (str): The year for which the average result is recorded.
        rank (int): The rank of the student based on the average score. Default is None.

    Methods:
        __init__(*args, **kwargs): Initializes the STUDSemesterRecord instance.
    """
    __tablename__ = 'student_semester_records'
    user_id: Mapped[str] = mapped_column(String(120), ForeignKey('users.id'), nullable=False)
    semester_id: Mapped[str] = mapped_column(String(120), ForeignKey(
        'semesters.id'), nullable=False)
    grade_id: Mapped[str] = mapped_column(String(120), ForeignKey('grades.id'), nullable=False)
    section_id: Mapped[str] = mapped_column(String(120), ForeignKey('sections.id'), nullable=True)
    year_record_id: Mapped[str] = mapped_column(String(120), ForeignKey('student_year_records.id'), nullable=True)
    average: Mapped[float] = mapped_column(Float, default=None)
    rank: Mapped[int] = mapped_column(Integer, default=None)
