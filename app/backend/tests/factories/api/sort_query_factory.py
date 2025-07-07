from typing import Any
from factory import LazyAttribute
from faker import Faker
from dataclasses import dataclass
from .typed_factory import TypedFactory

fake = Faker()


@dataclass
class SortQuery:
    tableId: str
    id: str
    desc: bool = False


class SortQueryFactory(TypedFactory[SortQuery]):
    class Meta:
        model = SortQuery
        exclude = ("sort_for",)

    # general fields helping defining others
    sort_for: Any = LazyAttribute(lambda _: None)

    id: Any = LazyAttribute(lambda x: next(iter(x.sort_for.items()))[0])
    tableId: Any = LazyAttribute(lambda x: next(iter(x.sort_for.items()))[1])
    desc: Any = LazyAttribute(lambda _: fake.boolean())

    def __init__(self, *args: Any, **kwargs: Any) -> Any:
        sort_for = kwargs.get("sort_for", self.sort_for)
        if not sort_for:
            raise ValueError("sort_for is required and cannot be None")

        # Call the parent constructor
        super().__init__(*args, **kwargs)
