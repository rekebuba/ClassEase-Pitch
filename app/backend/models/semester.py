#!/usr/bin/python3
""" Module for Section class """

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.engine.db_storage import BaseModel, Base


class Semester(BaseModel, Base):
    """docstring for Semester."""
    __tablename__ = 'semesters'
    name = Column(String(50), nullable=False)
    academic_year_EC = Column(Integer, nullable=False)
    academic_year_GC = Column(String(50), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    registration_start = Column(DateTime, nullable=False)
    registration_end = Column(DateTime, nullable=False)

    def __init__(self, *args, **kwargs):
        """ Initializes the registration instance. """
        super().__init__(*args, **kwargs)
