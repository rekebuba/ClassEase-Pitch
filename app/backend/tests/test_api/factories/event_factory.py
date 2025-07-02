import random
from typing import Any, Dict
from factory import LazyAttribute, SubFactory
from factory.fuzzy import FuzzyChoice
from faker import Faker
from datetime import datetime, timedelta
from pyethiodate import EthDate  # type: ignore
from models.event import Event
from .base_factory import BaseFactory
from .year_factory import YearFactory
from .semester_factory import SemesterFactory
from extension.enums.enum import (
    EventEligibilityEnum,
    EventLocationEnum,
    EventOrganizerEnum,
    EventPurposeEnum,
)

fake = Faker()


class EventFactory(BaseFactory[Event]):
    class Meta:
        model = Event

    _add_for_test: Dict[str, Any] = {
        "academic_year": lambda **kwarg: EthDate.date_to_ethiopian(datetime.now()).year,
        "semester": lambda **kwarg: SemesterFactory.build(),
    }

    year: Any = SubFactory(YearFactory)
    year_id: Any = LazyAttribute(lambda x: x.year.id)

    title: Any = LazyAttribute(lambda x: fake.sentence())
    purpose: Any = LazyAttribute(lambda x: FuzzyChoice(list(EventPurposeEnum)))

    organizer: Any = LazyAttribute(
        lambda obj: FuzzyChoice(list(EventOrganizerEnum))
        if obj.purpose != EventPurposeEnum.NEW_SEMESTER
        else EventOrganizerEnum.SCHOOL_ADMINISTRATION
    )

    start_date: Any = LazyAttribute(lambda x: fake.past_date())
    end_date: Any = LazyAttribute(lambda x: fake.future_date())
    start_time: Any = LazyAttribute(
        lambda x: datetime.now() - timedelta(hours=1)
    )  # Past datetime
    end_time: Any = LazyAttribute(
        lambda x: datetime.now() + timedelta(hours=1)
    )  # Future datetime

    location: Any = LazyAttribute(
        lambda obj: FuzzyChoice(EventLocationEnum)
        if obj.purpose != EventPurposeEnum.NEW_SEMESTER
        else EventLocationEnum.ONLINE
    )

    is_hybrid: Any = LazyAttribute(
        lambda obj: True if obj.location != EventLocationEnum.ONLINE else False
    )
    online_link: Any = LazyAttribute(lambda obj: fake.url() if obj.is_hybrid else None)

    eligibility: Any = LazyAttribute(
        lambda obj: FuzzyChoice(EventEligibilityEnum)
        if obj.purpose != EventPurposeEnum.NEW_SEMESTER
        else EventEligibilityEnum.ALL
    )

    has_fee: Any = LazyAttribute(
        lambda obj: fake.boolean()
        if obj.purpose != EventPurposeEnum.NEW_SEMESTER
        else True
    )
    fee_amount: Any = LazyAttribute(
        lambda obj: random.randint(100, 900) if obj.has_fee else 0.00
    )
    description: Any = LazyAttribute(lambda x: fake.text())
