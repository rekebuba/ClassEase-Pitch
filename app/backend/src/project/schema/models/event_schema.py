from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from project.schema.schema import BaseSchema
from project.utils.enum import (
    EventEligibilityEnum,
    EventLocationEnum,
    EventOrganizerEnum,
    EventPurposeEnum,
)

if TYPE_CHECKING:
    from project.schema.models.year_schema import YearSchema


class EventSchema(BaseSchema):
    """
    This model represents an event in the system.
    """

    id: uuid.UUID
    year_id: uuid.UUID
    title: str
    purpose: EventPurposeEnum
    organizer: EventOrganizerEnum
    start_date: date
    end_date: date
    start_time: datetime
    end_time: datetime
    location: Optional[EventLocationEnum] = None
    is_hybrid: bool = False
    online_link: Optional[str] = None
    eligibility: Optional[EventEligibilityEnum] = None
    has_fee: bool = False
    fee_amount: int = 0
    description: Optional[str] = None


class EventRelatedSchema(BaseSchema):
    """This model represents the relationships of a EventSchema."""

    year: Optional[YearSchema] = None


class EventWithRelatedSchema(EventSchema, EventRelatedSchema):
    """
    This model combines the EventSchema with its relationships.
    It is used to provide a complete view of an event along with related entities.
    """

    pass
