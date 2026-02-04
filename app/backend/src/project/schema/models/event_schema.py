from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict

from project.utils.enum import (
    EventEligibilityEnum,
    EventLocationEnum,
    EventOrganizerEnum,
    EventPurposeEnum,
)
from project.utils.utils import to_camel

if TYPE_CHECKING:
    from project.schema.models.year_schema import YearSchema


class EventSchema(BaseModel):
    """
    This model represents an event in the system.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    id: uuid.UUID | None = None
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


class EventRelatedSchema(BaseModel):
    """This model represents the relationships of a EventSchema."""

    year: Optional[YearSchema] = None


class EventWithRelatedSchema(EventSchema, EventRelatedSchema):
    """
    This model combines the EventSchema with its relationships.
    It is used to provide a complete view of an event along with related entities.
    """

    pass
