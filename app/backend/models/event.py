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
from extension.enums.enum import (
    EventEligibilityEnum,
    EventLocationEnum,
    EventOrganizerEnum,
    EventPurposeEnum,
)
from models.base.base_model import BaseModel
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING
from models.base.column_type import UUIDType
import uuid

if TYPE_CHECKING:
    from models.year import Year


class Event(BaseModel):
    """docstring for Event."""

    __tablename__ = "events"
    year_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(), ForeignKey("years.id", ondelete='CASCADE'), nullable=False
    )

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    purpose: Mapped[str] = mapped_column(
        String(50),
        Enum(
            EventPurposeEnum,
            name="event_purpose_enum",
            values_callable=lambda obj: [e.value for e in EventPurposeEnum],
            native_enum=False,
        ),
        nullable=False,
    )
    organizer: Mapped[str] = mapped_column(
        String(50),
        Enum(
            EventOrganizerEnum,
            name="event_organizer_enum",
            values_callable=lambda obj: [e.value for e in EventOrganizerEnum],
            native_enum=False,
        ),
        nullable=False,
    )

    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    start_time: Mapped[DateTime] = mapped_column(DateTime)
    end_time: Mapped[DateTime] = mapped_column(DateTime)

    location: Mapped[str] = mapped_column(
        String(50),
        Enum(
            EventLocationEnum,
            name="event_location_enum",
            values_callable=lambda obj: [e.value for e in EventLocationEnum],
            native_enum=False,
        ),
        nullable=True,
    )
    is_hybrid: Mapped[bool] = mapped_column(Boolean, default=False)
    online_link: Mapped[str] = mapped_column(Text, nullable=True, default=None)

    eligibility: Mapped[str] = mapped_column(
        String(50),
        Enum(
            EventEligibilityEnum,
            name="event_eligibility_enum",
            values_callable=lambda obj: [e.value for e in EventEligibilityEnum],
            native_enum=-False,
        ),
        nullable=True,
        default=None,
    )
    has_fee: Mapped[bool] = mapped_column(Boolean, default=False)
    fee_amount: Mapped[int] = mapped_column(Integer, default=0.00)

    description: Mapped[str] = mapped_column(String(255), nullable=True, default=None)

    # Relationships
    year: Mapped["Year"] = relationship(
        "Year",
        back_populates="events",
        default=None,
        repr=False,
        passive_deletes=True,
    )

    __table_args__ = (
        CheckConstraint("start_date <= end_date", name="check_event_dates"),
        CheckConstraint("start_time <= end_time", name="check_event_times"),
    )
