#!/usr/bin/python3
""" Module for Student class """

from sqlalchemy import Date, Integer, String, ForeignKey, CheckConstraint, Float, Boolean, Text, DateTime, case
from models.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text


class Student(BaseModel):
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
    __tablename__ = 'students'
    user_id: Mapped[str] = mapped_column(String(120), ForeignKey(
        'users.id'), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    father_name: Mapped[str] = mapped_column(String(50), nullable=False)
    grand_father_name: Mapped[str] = mapped_column(String(50), nullable=False)
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(1), nullable=False)

    # Parent/Guardian Contacts
    father_phone: Mapped[str] = mapped_column(String(25))
    mother_phone: Mapped[str] = mapped_column(String(25))
    guardian_name: Mapped[str] = mapped_column(
        String(50))  # If student lives with someone else
    guardian_phone: Mapped[str] = mapped_column(String(25))

    # Academic Info
    start_year_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('years.id'), nullable=False)
    current_year_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('years.id'), nullable=False)
    current_grade_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('grades.id'), nullable=False)
    next_grade_id: Mapped[str] = mapped_column(String(120), ForeignKey(
        'grades.id'), nullable=True, default=None)
    semester_id: Mapped[str] = mapped_column(
        String(120), ForeignKey('semesters.id'), nullable=True, default=None)
    has_passed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_registered: Mapped[bool] = mapped_column(Boolean, default=False)

    # If transferring from another school
    is_transfer: Mapped[bool] = mapped_column(Boolean, default=False)
    previous_school_name: Mapped[str] = mapped_column(
        String(100), nullable=True, default=None)

    # Identification & Legal Docs
    birth_certificate: Mapped[str] = mapped_column(
        String(255), nullable=True, default=None)  # Path to uploaded file

    # Health & Special Needs
    has_medical_condition: Mapped[bool] = mapped_column(Boolean, default=False)
    # Explanation of medical conditions
    medical_details: Mapped[str] = mapped_column(
        Text, nullable=True, default=None)
    has_disability: Mapped[bool] = mapped_column(Boolean, default=False)
    # Explanation of disabilities
    disability_details: Mapped[str] = mapped_column(
        Text, nullable=True, default=None)
    requires_special_accommodation: Mapped[bool] = mapped_column(
        Boolean, default=False)
    special_accommodation_details: Mapped[str] = mapped_column(
        Text, nullable=True, default=None)  # Any special support needed

    # Whether the student is currently enrolled
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates='student')
    student_semester_records = relationship(
        "STUDSemesterRecord", back_populates="student", cascade="all, delete-orphan")
    student_year_record = relationship(
        "STUDYearRecord", back_populates="student", cascade="all, delete-orphan")
    average_subject = relationship(
        "AverageSubject", back_populates="student", cascade="all, delete-orphan")
