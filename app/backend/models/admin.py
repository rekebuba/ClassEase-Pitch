#!/usr/bin/python3
""" Module for Admin class """

from sqlalchemy import CheckConstraint, Column, Date, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Admin(BaseModel, Base):
    """
    Admin Model

    This model represents an admin in the system. It inherits from BaseModel and Base.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        id (str): The unique identifier for the admin, which is a foreign key referencing the users table.
        name (str): The name of the admin. This field is required.
        email (str): The email of the admin. This field is required and must be unique.

    Methods:
        __init__(*args, **kwargs): Initializes the admin instance.
    """
    __tablename__ = 'admin'
    user_id = Column(String(120), ForeignKey(
        'users.id'), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    father_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(1), nullable=False)
    email = Column(String(120), nullable=False)
    phone = Column(String(25), nullable=False)
    address = Column(String(120), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "gender IN ('M', 'F')",
            name="check_admin_gender"
        ),
    )

    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
