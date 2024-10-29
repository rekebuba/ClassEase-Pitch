#!/usr/bin/python3
""" Module for User class """

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from ethiopian_date import EthiopianDateConverter
import random
from datetime import datetime


class User(BaseModel, Base):
    """
    User Model

    This module defines the User model which represents a user in the system. The User can have one of three roles: 'admin', 'teacher', or 'student'. Each user has a unique ID and a password.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        id (Column): The unique identifier for the user.
        password (Column): The password for the user.
        role (Column): The role of the user, which can be 'admin', 'teacher', or 'student'.

    Methods:
        __init__(*args, **kwargs): Initializes the User instance and generates a custom ID based on the role.
        generate_id(role): Generates a custom ID based on the role (Admin, Student, Teacher).
        id_exists(id): Checks if the generated ID already exists in the users table.
    """
    __tablename__ = 'users'
    id = Column(String(120), primary_key=True, unique=True)
    password = Column(String(120), nullable=False)
    role = Column(String(50), nullable=False)



    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the class.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Attributes:
            id (str): The unique identifier generated based on the user's role.
        """
        """initializes score"""
        super().__init__(*args, **kwargs)
        self.id = self.generate_id(self.role)

    def generate_id(self, role):
        """
        Generates a custom ID based on the role (Admin, Student, Teacher).

        The ID format is: <section>/<random_number>/<year_suffix>
        - Section: 'MAS' for Student, 'MAT' for Teacher, 'MAA' for Admin
        - Random number: A 4-digit number between 1000 and 9999
        - Year suffix: Last 2 digits of the current Ethiopian year

        Args:
            role (str): The role of the user ('Student', 'Teacher', 'Admin').

        Returns:
            str: A unique custom ID.
        """
        id = ''
        section = ''

        # Assign prefix based on role
        if role == 'Student':
            section = 'MAS'
        elif role == 'Teacher':
            section = 'MAT'
        elif role == 'Admin':
            section = 'MAA'

        unique = True
        while unique:
            num = random.randint(1000, 9999)
            starting_year = EthiopianDateConverter.date_to_ethiopian(
                datetime.now()).year % 100  # Get last 2 digits of the year
            id = f'{section}/{num}/{starting_year}'

            # Check if the generated ID already exists in the users table
            if not self.id_exists(id):
                unique = False

        return id


    def id_exists(self, id):
        """
        Checks if the generated ID already exists in the users table.

        Args:
            id (str): The ID to check for existence in the users table.

        Returns:
            bool: True if the ID exists in the users table, False otherwise.
        """
        """Checks if the generated ID already exists in the users table"""
        from models import storage
        # Check in the `users` table for the ID
        if storage.get_first(User, id=id):
            return True
        return False
