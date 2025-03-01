#!/usr/bin/python3
""" Module for Student class """

from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, Float, Boolean, Text, DateTime
from models.engine.db_storage import BaseModel, Base
from sqlalchemy.orm import relationship

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
    user_id = Column(String(120), ForeignKey('users.id'), unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    father_name = Column(String(50), nullable=False)
    grand_father_name = Column(String(50), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)

    # Parent/Guardian Contacts
    father_phone = Column(String(25))
    mother_phone = Column(String(25))
    guardian_name = Column(String(50))  # If student lives with someone else
    guardian_phone = Column(String(25))

    # Academic Info
    start_year_EC = Column(String(15), nullable=False)
    start_year_GC = Column(String(15), nullable=False)
    end_year = Column(String(10))

    # If transferring from another school
    previous_school = Column(String(100))

    # Academic Performance
    current_grade = Column(Integer, nullable=False)
    semester_id = Column(String(120), ForeignKey('semesters.id'))
    has_passed = Column(Boolean, default=False)
    registration_window_start = Column(DateTime)

    # Identification & Legal Docs
    birth_certificate = Column(String(255))  # Path to uploaded file
    national_id = Column(String(50))  # Optional national ID/passport

    # Health & Special Needs
    has_medical_condition = Column(Boolean, default=False)
    medical_details = Column(Text)  # Explanation of medical conditions
    has_disability = Column(Boolean, default=False)
    disability_details = Column(Text)  # Explanation of disabilities
    requires_special_accommodation = Column(Boolean, default=False)
    special_accommodation_details = Column(Text)  # Any special support needed

    # Student Status
    is_transferring = Column(Boolean, default=False)

    # Whether the student is currently enrolled
    is_active = Column(Boolean, default=True)

    __table_args__ = (
        CheckConstraint(
            'father_phone IS NOT NULL OR mother_phone IS NOT NULL OR guardian_phone IS NOT NULL',
            name='at_least_one_contact'
        ),
    )

    # # Relationships
    # # If linked to a User table
    # user = relationship("User", back_populates="student")

    def __init__(self, *args, **kwargs):
        """
        Initializes the score.

        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
