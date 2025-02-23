#!/usr/bin/python3
""" Module for Section class """

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.engine.db_storage import BaseModel, Base


class Registration(BaseModel, Base):
    """docstring for Registration."""
    __tablename__ = 'registrations'
    student_id = Column(String(120), ForeignKey('student.id'), nullable=False)
    subject_id = Column(String(120), ForeignKey('subjects.id'), nullable=False)
    registration_date = Column(DateTime, nullable=False)

    def __init__(self, *args, **kwargs):
        """ Initializes the registration instance. """
        super().__init__(*args, **kwargs)
