#!/usr/bin/python3

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.engine.db_storage import BaseModel, Base


class Section(BaseModel, Base):
    __tablename__ = 'sections'
    grade_id = Column(String(60), ForeignKey('grades.id'))
    name = Column(String(1)) # e.g., A, B, C, D, E, F, G
    # teacher = Column(String(100), nullable=False)
    # teacher_id = Column(Integer, ForeignKey('teachers.id'))

    # Define relationships
    students = relationship("Student", backref="section", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
