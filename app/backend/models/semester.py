#!/usr/bin/python3
""" Module for Section class """

from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.engine.db_storage import BaseModel, Base


class Semester(BaseModel, Base):
    """docstring for Semester."""
    __tablename__ = 'semesters'
    event_id = Column(String(225), ForeignKey('events.id'), nullable=False)
    name = Column(String(50), nullable=False)
    academic_year_EC = Column(Integer, nullable=False)
    academic_year_GC = Column(String(50))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    registration_start = Column(Date, nullable=False)
    registration_end = Column(Date, nullable=False)

    def __init__(self, *args, **kwargs):
        """ Initializes the registration instance. """
        super().__init__(*args, **kwargs)
