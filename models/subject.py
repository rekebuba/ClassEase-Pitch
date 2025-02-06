#!/usr/bin/python3
""" Module for Subject class """

from sqlalchemy import Column, Integer, String, ForeignKey
from models.engine.db_storage import BaseModel, Base


class Subject(BaseModel, Base):
    """
    Subject Model

    This model represents a subject in the ClassEase system. It includes the subject's name, code, associated grade, and year.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        name (Column): The name of the subject, limited to 50 characters, cannot be null.
        code (Column): The code of the subject, limited to 10 characters, cannot be null.
        grade_id (Column): Foreign key linking to the grade, cannot be null.
        year (Column): The academic year of the subject, limited to 10 characters, cannot be null.

    Methods:
        __init__(*args, **kwargs): Initializes the subject with variable length arguments and keyword arguments.
    """
    __tablename__ = 'subjects'
    name = Column(String(50), nullable=False)
    code = Column(String(10), nullable=False, unique=True)
    grade_id = Column(String(120), ForeignKey('grades.id'), nullable=False)
    year = Column(String(10), nullable=False)

    def __init__(self, *args, **kwargs):
        """
        Initializes the score.

        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
