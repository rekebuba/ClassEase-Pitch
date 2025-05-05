#!/usr/bin/python3
"""Module for Section class"""

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Text,
    String,
    Integer,
    Boolean,
    Date,
    DateTime,
    Enum,
)
from sqlalchemy.orm import Mapped, mapped_column
from models.base_model import BaseModel


class Event(BaseModel):
    """docstring for Semester."""

    __tablename__ = "events"
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    purpose: Mapped[str] = mapped_column(
        String(50),
        Enum(
            "Academic",
            "Cultural",
            "Sports",
            "Graduation",
            "Administration",
            "New Semester",
            "Other",
        ),
        nullable=False,
    )
    organizer: Mapped[str] = mapped_column(
        String(50),
        Enum("School Administration", "School", "Student Club", "External Organizer"),
        nullable=False,
    )

    year_id: Mapped[str] = mapped_column(
        String(125), ForeignKey("years.id"), nullable=False
    )

    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    start_time: Mapped[DateTime] = mapped_column(DateTime)
    end_time: Mapped[DateTime] = mapped_column(DateTime)

    location: Mapped[str] = mapped_column(
        String(50),
        Enum("Auditorium", "Classroom", "Sports Field", "Online", "Other"),
        nullable=True,
    )
    is_hybrid: Mapped[bool] = mapped_column(Boolean, default=False)
    online_link: Mapped[str] = mapped_column(Text, nullable=True, default=None)

    requires_registration: Mapped[bool] = mapped_column(Boolean, default=False)
    registration_start: Mapped[Date] = mapped_column(Date, nullable=True, default=None)
    registration_end: Mapped[Date] = mapped_column(Date, nullable=True, default=None)

    eligibility: Mapped[str] = mapped_column(
        String(50),
        Enum("All", "Students Only", "Faculty Only", "Invitation Only"),
        nullable=True,
        default=None,
    )
    has_fee: Mapped[bool] = mapped_column(Boolean, default=False)
    fee_amount: Mapped[int] = mapped_column(Integer, default=0.00)

    description: Mapped[str] = mapped_column(String(255), nullable=True, default=None)

    __table_args__ = (
        CheckConstraint("start_date <= end_date", name="check_event_dates"),
        CheckConstraint("start_time <= end_time", name="check_event_times"),
        CheckConstraint(
            "registration_start <= registration_end", name="check_registration_dates"
        ),
        CheckConstraint("fee_amount >= 0", name="check_fee_amount"),
        CheckConstraint(
            "requires_registration = True AND registration_start IS NOT NULL AND registration_end IS NOT NULL",
            name="check_registration_with_dates",
        ),
        CheckConstraint("has_fee = True AND fee_amount > 0", name="check_fee"),
        CheckConstraint(
            "purpose = 'New Semester' AND organizer = 'School Administration'",
            name="check_purpose_with_organizer",
        ),
        CheckConstraint(
            "purpose = 'New Semester' AND location = 'Online'",
            name="check_purpose_with_location",
        ),
        CheckConstraint(
            "purpose = 'New Semester' AND has_fee = True", name="check_purpose_with_fee"
        ),
        CheckConstraint(
            "purpose = 'New Semester' AND requires_registration = True",
            name="check_purpose_with_registration",
        ),
        CheckConstraint(
            "purpose = 'New Semester' AND eligibility = 'All'",
            name="check_purpose_with_eligibility",
        ),
        CheckConstraint(
            "purpose = 'New Semester' AND registration_start IS NOT NULL",
            name="check_purpose_with_registration_start",
        ),
        CheckConstraint(
            "purpose = 'New Semester' AND registration_end IS NOT NULL",
            name="check_purpose_with_registration_end",
        ),
    )
