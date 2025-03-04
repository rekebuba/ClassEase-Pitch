#!/usr/bin/python3
""" Module for Section class """

from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.engine.db_storage import BaseModel, Base


class Semester(BaseModel, Base):
    """docstring for Semester."""
    __tablename__ = 'semesters'
    event_id = Column(String(225), ForeignKey('events.id'), nullable=False)
    name = Column(Integer, nullable=False)

    def __init__(self, *args, **kwargs):
        """ Initializes the registration instance. """
        super().__init__(*args, **kwargs)
