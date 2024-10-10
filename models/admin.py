#!/usr/bin/python3

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Admin(BaseModel, Base):
    __tablename__ = 'admin'
    id = Column(String(120), ForeignKey('users.id'), primary_key=True, unique=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False, unique=True)

    # Inherit id, password from User Table

    # Define relationships
    # grades = relationship("Grade", backref="user", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
