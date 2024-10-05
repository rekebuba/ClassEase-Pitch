#!/usr/bin/python3

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.engine.db_storage import BaseModel, Base


class Grade(BaseModel, Base):
    __tablename__ = 'grades'
    name = Column(Integer, nullable=False)
    # teacher = Column(String(100), nullable=False)
    # section = Column(String(1), nullable=False)  # e.g., A, B, C, D, E, F, G
    # teacher_id = Column(Integer, ForeignKey('teachers.id'))

    # Define relationships
    section = relationship("Section", backref="grade", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
