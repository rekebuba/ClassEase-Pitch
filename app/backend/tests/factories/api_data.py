import random
import uuid
from typing import get_args

from factory import LazyAttribute
from faker import Faker

from api.v1.routers.year.schema import NewYear
from tests.factories.typed_factory import TypedFactory
from utils.enum import AcademicTermTypeEnum, AcademicYearStatusEnum
from utils.type import SetupMethodType

fake = Faker()


class NewYearFactory(TypedFactory[NewYear]):
    class Meta:
        model = NewYear

    name = LazyAttribute(lambda _: fake.name())
    calendar_type = LazyAttribute(lambda _: random.choice(list(AcademicTermTypeEnum)))
    start_date = LazyAttribute(lambda _: fake.past_date())
    end_date = LazyAttribute(lambda _: fake.future_date())
    status = LazyAttribute(
        lambda _: random.choice(
            [AcademicYearStatusEnum.ACTIVE, AcademicYearStatusEnum.UPCOMING]
        )
    )
    setup_methods = LazyAttribute(lambda _: random.choice(get_args(SetupMethodType)))
    copy_from_year_id = LazyAttribute(
        lambda x: uuid.uuid4() if x.setup_methods == "Last Year Copy" else None
    )
