from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, ConfigDict
from datetime import date, datetime

from extension.enums.enum import (
    EventEligibilityEnum,
    EventLocationEnum,
    EventOrganizerEnum,
    EventPurposeEnum,
)
from extension.functions.helper import to_camel

if TYPE_CHECKING:
    from .year_schema import YearSchema


class EventSchema(BaseModel):
    """
    This model represents an event in the system.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    year_id: str
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


class EventRelationshipSchema(BaseModel):
    """This model represents the relationships of a EventSchema."""

    year: Optional[YearSchema] = None
