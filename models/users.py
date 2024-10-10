#!/usr/bin/python3

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from ethiopian_date import EthiopianDateConverter
import random
from datetime import datetime


class User(BaseModel, Base):
    __tablename__ = 'users'
    id = Column(String(120), primary_key=True, unique=True)
    password = Column(String(120), nullable=False)
    # Can be 'admin', 'teacher', or 'student'
    role = Column(String(50), nullable=False)

    # Define relationships
    # grades = relationship("Grade", backref="user", cascade="all, delete-orphan")


    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
        self.id = self.generate_id(self.role)

    def generate_id(self, role):
        """Generates a custom ID based on the role (Admin, Student, Teacher)"""
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
        """Checks if the generated ID already exists in the users table"""
        from models import storage
        # Check in the `users` table for the ID
        if storage.get_first(User, id=id):
            return True
        return False
