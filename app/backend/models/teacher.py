#!/usr/bin/python3
""" Module for Teacher class """

from sqlalchemy import CheckConstraint, Date, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel


class Teacher(BaseModel):
    """
    Teacher Model
    This model represents a teacher in the ClassEase system. It inherits from BaseModel and Base.
    Attributes:
        __tablename__ (str): The name of the table in the database.
        id (str): The unique identifier for the teacher, which is a foreign key referencing the users table.
        first_name (str): The first name of the teacher.
        last_name (str): The last name of the teacher.
        gender (str): The gender of the teacher.
        age (str): The age of the teacher.
        email (str): The email address of the teacher.
        phone (str): The phone number of the teacher.
        address (str): The address of the teacher.
        experience (int): The number of years of experience the teacher has.
        qualification (str): The qualification of the teacher.
        subject_taught (str): The subject that the teacher teaches.
        no_of_mark_list (int): The number of mark lists associated with the teacher. Defaults to 0.
    Methods:
        __init__(*args, **kwargs): Initializes the Teacher instance.
    """
    __tablename__ = 'teachers'
    user_id: Mapped[str] = mapped_column(String(120), ForeignKey(
        'users.id'), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    father_name: Mapped[str] = mapped_column(String(50), nullable=False)
    grand_father_name: Mapped[str] = mapped_column(String(50), nullable=False)
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(1), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(25), nullable=False)
    address: Mapped[str] = mapped_column(String(120), nullable=False)
    year_of_experience: Mapped[int] = mapped_column(Integer, nullable=False)
    qualification: Mapped[str] = mapped_column(String(120), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "gender IN ('M', 'F')",
            name="check_teacher_gender"
        ),
        CheckConstraint(
            "year_of_experience >= 0",
            name="check_teacher_experience"
        )
    )
