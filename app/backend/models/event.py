#!/usr/bin/python3
""" Module for Section class """

from sqlalchemy import CheckConstraint, Column, ForeignKey, Text, String, Integer, Boolean, Date, DateTime, Enum
from sqlalchemy.orm import relationship
from models.engine.db_storage import BaseModel, Base


class Event(BaseModel, Base):
    """docstring for Semester."""
    __tablename__ = 'events'
    title = Column(String(100), nullable=False)
    purpose = Column(String(50), Enum('Academic', 'Cultural', 'Sports', 'Graduation',
                     'Administration', 'New Semester', 'Other'), nullable=False)
    organizer = Column(String(50), Enum('School Administration',
                       'School', 'Student Club', 'External Organizer'), nullable=False)

    # ethiopian_year = Column(String(10), nullable=False)
    # gregorian_year = Column(String(15), default=None, nullable=True)
    year_id = Column(String(225), ForeignKey('years.id'), nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    location_type = Column(String(50), Enum(
        'Auditorium', 'Classroom', 'Sports Field', 'Online', 'Other'), nullable=True)
    is_hybrid = Column(Boolean, default=False)
    online_link = Column(Text, nullable=True)

    requires_registration = Column(Boolean, default=False)
    registration_start = Column(Date, nullable=True)
    registration_end = Column(Date, nullable=True)

    eligibility = Column(String(50), Enum(
        'All', 'Students Only', 'Faculty Only', 'Invitation Only'), nullable=True)
    has_fee = Column(Boolean, default=False)
    fee_amount = Column(Integer, default=0.00)

    description = Column(String(255), nullable=True)

    __table_args__ = (
        CheckConstraint(
            "start_date <= end_date",
            name="check_event_dates"
        ),
        CheckConstraint(
            "start_time <= end_time",
            name="check_event_times"
        ),
        CheckConstraint(
            "registration_start <= registration_end",
            name="check_registration_dates"
        ),
        CheckConstraint(
            "fee_amount >= 0",
            name="check_fee_amount"
        ),
        CheckConstraint(
            "location_type = 'Online' AND online_link IS NOT NULL",
            name="check_online_link"
        ),
        CheckConstraint(
            "requires_registration = True AND registration_start IS NOT NULL AND registration_end IS NOT NULL",
            name="check_registration_with_dates"
        ),
        CheckConstraint(
            "has_fee = True AND fee_amount > 0",
            name="check_fee"
        ),
        CheckConstraint(
            "is_hybrid = True AND location_type = 'Online'",
            name="check_hybrid"
        ),
        CheckConstraint(
            "purpose = 'New Semester' AND organizer = 'School Administration'",
            name="check_purpose_with_organizer"
        ),
        CheckConstraint(
            "purpose = 'New Semester' AND location_type = 'Online'",
            name="check_purpose_with_location"
        ),
        CheckConstraint(
            "purpose = 'New Semester' AND has_fee = True",
            name="check_purpose_with_fee"
        ),
        CheckConstraint(
            "purpose = 'New Semester' AND requires_registration = True",
            name="check_purpose_with_registration"
        ),
        CheckConstraint(
            "purpose = 'New Semester' AND eligibility = 'All'",
            name="check_purpose_with_eligibility"
        ),
        CheckConstraint(
            "purpose = 'New Semester' AND is_hybrid = True",
            name="check_purpose_with_hybrid"
        ),
        CheckConstraint(
            "purpose = 'New Semester' AND registration_start IS NOT NULL",
            name="check_purpose_with_registration_start"
        ),
        CheckConstraint(
            "purpose = 'New Semester' AND registration_end IS NOT NULL",
            name="check_purpose_with_registration_end"
        )
    )

    def __init__(self, *args, **kwargs):
        """ Initializes the registration instance. """
        super().__init__(*args, **kwargs)
