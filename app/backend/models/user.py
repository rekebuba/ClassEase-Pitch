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
    identification = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    role = Column(String(50), nullable=False)
    image_path = Column(String(255), nullable=True)
    national_id = Column(String(120), nullable=False)

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the class.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Attributes:
            identification (str): The unique identifier generated based on the user's role.
        """
        super().__init__(*args, **kwargs)
