#!/usr/bin/python3
""" Module for User class """

from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel


class User(BaseModel):
    """
    User Model

    This module defines the User model which represents a user in the system. The User can have one of three roles: 'admin', 'teacher', or 'student'. Each user has a unique ID and a password.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        id (mapped_column): The unique identifier for the user.
        password (mapped_column): The password for the user.
        role (mapped_column): The role of the user, which can be 'admin', 'teacher', or 'student'.

    """
    __tablename__ = 'users'
    identification: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[BaseModel.RoleEnum] = mapped_column(
        Enum(BaseModel.RoleEnum), nullable=False)
    image_path: Mapped[str] = mapped_column(String(255), nullable=True)
    national_id: Mapped[str] = mapped_column(String(120), nullable=False)

    admin = relationship('Admin', back_populates='user', uselist=False)
