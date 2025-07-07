import random
from typing import Any, Optional, Callable, Dict
from factory import LazyAttribute
from dataclasses import dataclass
from datetime import date, datetime
from faker import Faker
from .typed_factory import TypedFactory

fake = Faker()


@dataclass
class MinMax:
    min: Optional[float | int] = None
    max: Optional[float | int] = None

    def __post_init__(self):
        if self.min is not None and self.max is not None and self.min > self.max:
            raise ValueError("min cannot be greater than max")


# Helper for MinMaxFactory
MINMAX_GENERATE: Dict[type, Callable[[int, int], Any]] = {
    int: lambda x, y: random.randint(x, y),
    float: lambda x, y: round(random.uniform(x, y), 2),
    date: lambda x, y: str(
        fake.date_between(
            x if isinstance(x, date) else datetime.strptime(str(x), "%Y-%m-%d").date(),
            y if isinstance(y, date) else datetime.strptime(str(y), "%Y-%m-%d").date(),
        )
    ),
}


class MinMaxFactory(TypedFactory[MinMax]):
    class Meta:
        model = MinMax
        exclude = ("type", "lowest", "highest")

    # general fields helping defining others
    type: Any = LazyAttribute(lambda _: None)
    lowest: Any = LazyAttribute(lambda _: 0)
    highest: Any = LazyAttribute(lambda _: 100)

    min: Any = LazyAttribute(lambda x: MINMAX_GENERATE.get(x.type)(x.lowest, x.highest))
    max: Any = LazyAttribute(lambda x: MINMAX_GENERATE.get(x.type)(x.min, x.highest))
