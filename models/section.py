#!/usr/bin/python3

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.engine.db_storage import BaseModel, Base


class Section(BaseModel, Base):
    __tablename__ = 'sections'
    section = Column(String(1)) # e.g., A, B, C, D, E, F, G
    grade_id = Column(String(120), ForeignKey('grades.id'), nullable=False)


    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
