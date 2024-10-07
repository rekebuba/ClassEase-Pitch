#!/usr/bin/python3

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.engine.db_storage import BaseModel, Base


class Grade(BaseModel, Base):
    __tablename__ = 'grades'
    grade = Column(Integer, nullable=False)

    # Define relationships
    section = relationship("Section", backref="grade", cascade="all, delete-orphan")
    subject = relationship("Subject", backref="grade", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes score"""
        super().__init__(*args, **kwargs)
