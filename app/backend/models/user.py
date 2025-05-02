#!/usr/bin/python3
""" Module for User class """

from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel


class User(BaseModel):
    """
    This module defines the User model which represents a user in the system. The User can have one of three roles: 'admin', 'teacher', or 'student'. Each user has a unique ID and a password.
    """
    __tablename__ = 'users'
    identification: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[BaseModel.RoleEnum] = mapped_column(
        Enum(BaseModel.RoleEnum), nullable=False)
    image_path: Mapped[str] = mapped_column(String(255), nullable=True)
    national_id: Mapped[str] = mapped_column(String(120), nullable=False)

    # One-to-many relationship
    admins = relationship('Admin', back_populates='user', uselist=False)
    teachers = relationship('Teacher', back_populates='user', uselist=False)
    students = relationship("Student", back_populates='user', uselist=False)
