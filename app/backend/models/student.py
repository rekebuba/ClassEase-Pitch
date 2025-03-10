#!/usr/bin/python3
""" Module for Student class """

from sqlalchemy import Column, Date, Integer, String, ForeignKey, CheckConstraint, Float, Boolean, Text, DateTime, case
from models.engine.db_storage import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text


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
    user_id = Column(String(120), ForeignKey(
        'users.id'), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    father_name = Column(String(50), nullable=False)
    grand_father_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(1), nullable=False)

    # Parent/Guardian Contacts
    father_phone = Column(String(25))
    mother_phone = Column(String(25))
    guardian_name = Column(String(50))  # If student lives with someone else
    guardian_phone = Column(String(25))

    # Academic Info
    start_year_id = Column(String(120), nullable=False)
    current_year_id = Column(String(120), nullable=False)

    # If transferring from another school
    is_transfer = Column(Boolean, default=False)
    previous_school_name = Column(String(100), default=None)

    # Academic Performance
    current_grade = Column(Integer, nullable=False)
    semester_id = Column(String(120), ForeignKey('semesters.id'))
    has_passed = Column(Boolean, default=False)
    next_grade = Column(Integer, nullable=True, default=None)
    is_registered = Column(Boolean, default=False)

    # Identification & Legal Docs
    birth_certificate = Column(
        String(255), nullable=True, default=None)  # Path to uploaded file

    # Health & Special Needs
    has_medical_condition = Column(Boolean, default=False)
    medical_details = Column(Text, nullable=True)  # Explanation of medical conditions
    has_disability = Column(Boolean, default=False)
    disability_details = Column(Text, nullable=True)  # Explanation of disabilities
    requires_special_accommodation = Column(Boolean, default=False)
    special_accommodation_details = Column(Text, nullable=True)  # Any special support needed

    # Whether the student is currently enrolled
    is_active = Column(Boolean, default=False)

    def __init__(self, *args, **kwargs):
        """
        Initializes the score.

        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
