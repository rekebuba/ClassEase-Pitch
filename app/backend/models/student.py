#!/usr/bin/python3
""" Module for Student class """

from sqlalchemy import Column, Date, Integer, String, ForeignKey, CheckConstraint, Float, Boolean, Text, DateTime, case
from models.engine.db_storage import BaseModel, Base
from sqlalchemy.orm import relationship
from flask import current_app
from sqlalchemy.sql import text

is_mysql = "mysql" in str(current_app.config['SQLALCHEMY_DATABASE_URI'])


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
    start_year_ethiopian = Column(String(15), nullable=False)
    start_year_gregorian = Column(String(15), nullable=False)
    end_year_ethiopian = Column(String(15), default=None)
    end_year_gregorian = Column(String(15), default=None)

    # If transferring from another school
    is_transfer = Column(Boolean, default=False)
    previous_school_name = Column(String(100), default=None)

    # Academic Performance
    current_grade = Column(Integer, nullable=False)
    semester_id = Column(String(120), ForeignKey('semesters.id'))
    has_passed = Column(Boolean, default=False)

    # Identification & Legal Docs
    birth_certificate = Column(
        String(255), nullable=True, default=None)  # Path to uploaded file

    # Health & Special Needs
    has_medical_condition = Column(Boolean, default=False)
    medical_details = Column(Text)  # Explanation of medical conditions
    has_disability = Column(Boolean, default=False)
    disability_details = Column(Text)  # Explanation of disabilities
    requires_special_accommodation = Column(Boolean, default=False)
    special_accommodation_details = Column(Text)  # Any special support needed

    # Whether the student is currently enrolled
    is_active = Column(Boolean, default=False)

    __table_args__ = (

        CheckConstraint(
            'father_phone IS NOT NULL OR mother_phone IS NOT NULL OR guardian_phone IS NOT NULL',
            name='at_least_one_contact'
        ),
        CheckConstraint(
            'current_grade >= 1 AND current_grade <= 12',
            name='valid_grade_range'
        ),
        CheckConstraint(
            'gender IN ("M", "F")',
            name='check_student_gender'
        ),
        CheckConstraint(
            'start_year_ethiopian IS NOT NULL AND start_year_gregorian IS NOT NULL',
            name='check_start_year'
        ),
        CheckConstraint(
            case(
                (is_mysql, text("is_transfer = TRUE AND previous_school_name IS NOT NULL")),
                else_=text(
                    "is_transfer = 1 AND previous_school_name IS NOT NULL")
            ),
            name='check_previous_school'
        ),
        CheckConstraint(
            'is_transfer = FALSE AND previous_school_name IS NULL',
            name='check_previous_school_null'
        ),
        CheckConstraint(
            'has_medical_condition = True AND medical_details IS NOT NULL',
            name='check_medical_condition'
        ),
        CheckConstraint(
            'has_medical_condition = FALSE AND medical_details IS NULL',
            name='check_medical_condition_null'
        ),
        CheckConstraint(
            'has_disability = True AND disability_details IS NOT NULL',
            name='check_disability'
        ),
        CheckConstraint(
            'has_disability = False AND disability_details IS NULL',
            name='check_disability_null'
        ),
        CheckConstraint(
            'requires_special_accommodation = True AND special_accommodation_details IS NOT NULL',
            name='check_special_accommodation'
        ),
        CheckConstraint(
            'requires_special_accommodation = False AND special_accommodation_details IS NULL',
            name='check_special_accommodation_null'
        )
    )

    def __init__(self, *args, **kwargs):
        """
        Initializes the score.

        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
