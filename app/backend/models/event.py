#!/usr/bin/python3
""" Module for Section class """

from sqlalchemy import Column, String, Integer, Boolean, Date, DateTime, Enum
from sqlalchemy.orm import relationship
from models.engine.db_storage import BaseModel, Base


class Event(BaseModel, Base):
    """docstring for Semester."""
    __tablename__ = 'events'
    event_name = Column(String(255), nullable=False)
    purpose = Column(String(50), Enum('Academic', 'Cultural', 'Sports', 'Administration', 'New Semester', 'Other'), nullable=False)
    organizer = Column(String(50), Enum('School', 'Student Club', 'External Organizer'), nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    location_type = Column(String(50), Enum('Auditorium', 'Classroom', 'Sports Field', 'Online', 'Other'), nullable=True)
    is_hybrid = Column(Boolean, default=False)
    online_link = Column(String(255), nullable=True)

    requires_registration = Column(Boolean, default=False)
    registration_start = Column(Date, nullable=True)
    registration_end = Column(Date, nullable=True)

    eligibility = Column(String(50), Enum('All', 'Students Only', 'Faculty Only', 'Invitation Only'), nullable=True)
    has_fee = Column(Boolean, default=False)
    fee_amount = Column(Integer, default=0.00)

    description = Column(String(255), nullable=True)


    def __init__(self, *args, **kwargs):
        """ Initializes the registration instance. """
        super().__init__(*args, **kwargs)
