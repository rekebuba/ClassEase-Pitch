#!/usr/bin/python3
""" Module for Student class """

from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, Float, DateTime
from models.engine.db_storage import BaseModel, Base


class Student(BaseModel, Base):
    """
    Represents a student entity in the database.

    Attributes:
        id (str): Unique identifier for the student, linked to the 'users' table.
        name (str): Name of the student.
        father_name (str): Name of the student's father.
        grand_father_name (str): Name of the student's grandfather.
        date_of_birth (datetime): Date of birth of the student.
        father_phone (str): Phone number of the student's father.
        mother_phone (str): Phone number of the student's mother.
        start_year (str): The year the student started.
        end_year (str): The year the student ended.

    Constraints:
        At least one of 'father_phone' or 'mother_phone' must be provided.

    Methods:
        __init__(*args, **kwargs): Initializes a new instance of the Student class.
    """
    __tablename__ = 'student'
    id = Column(String(120), ForeignKey('users.id'), primary_key=True, unique=True)
    name = Column(String(50), nullable=False)
    father_name = Column(String(50), nullable=False)
    grand_father_name = Column(String(50))
    date_of_birth = Column(DateTime, nullable=False)
    father_phone = Column(String(25))
    mother_phone = Column(String(25))

    start_year = Column(String(10), nullable=False)
    end_year = Column(String(10))

    __table_args__ = (
        CheckConstraint(
            'father_phone IS NOT NULL OR mother_phone IS NOT NULL'),
    )


    def __init__(self, *args, **kwargs):
        """
        Initializes the score.

        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
