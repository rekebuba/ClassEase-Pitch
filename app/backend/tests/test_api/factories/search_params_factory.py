import random
from typing import Any, List, Dict
from factory import LazyAttribute
from dataclasses import dataclass, field
from .typed_factory import TypedFactory
from .sort_query_factory import SortQuery, SortQueryFactory
from .filter_query_factory import FilterQuery, FilterQueryFactory


@dataclass
class SearchParams:
    page: int
    per_page: int
    join_operator: str
    sort_test_ids: str
    sort: List[SortQuery] = field(default_factory=list)
    filters: List[FilterQuery] = field(default_factory=list)


class RandomNoRepeat:
    def __init__(self, values: List[Any]) -> None:
        self.original = values[:]
        self.remaining = values[:]

    def __call__(self):
        if not self.remaining:
            # Optionally, you can reset here
            self.remaining = self.original[:]
            # Or raise an error: raise StopIteration("No more values to return.")

        choice = random.choice(self.remaining)
        self.remaining.remove(choice)
        return choice


class SearchParamsFactory(TypedFactory[SearchParams]):
    class Meta:
        model = SearchParams
        exclude = (
            "tableId",
            "get_sort",
            "get_filter",
            "create_sort",
            "create_filter",
            "sort_many",
            "filters_many",
        )

    @staticmethod
    def generate_sort_queries(tableId: Dict[str, str], create: int) -> List[SortQuery]:
        picker = RandomNoRepeat(list(tableId.items()))

        queries: List[SortQuery] = []
        for _ in range(create):
            random_pair = picker()
            sort_for = dict([random_pair])
            queries.append(SortQueryFactory.create(sort_for=sort_for))

        return queries

    # general fields helping defining others
    tableId: Any = LazyAttribute(lambda _: None)
    get_sort: Any = LazyAttribute(lambda _: False)
    get_filter: Any = LazyAttribute(lambda _: False)
    sort_many: Any = LazyAttribute(lambda _: False)
    filters_many: Any = LazyAttribute(lambda _: False)
    create_sort: Any = LazyAttribute(
        lambda x: random.randint(1, len(x.tableId)) if x.sort_many else 1
    )
    create_filter: Any = LazyAttribute(
        lambda x: random.randint(1, len(x.tableId)) if x.filters_many else 1
    )

    page: Any = LazyAttribute(lambda _: 1)
    per_page: Any = LazyAttribute(lambda _: random.choice([10, 20, 30, 40, 50]))
    join_operator: Any = LazyAttribute(lambda _: random.choice(["and", "or"]))
    sort: Any = LazyAttribute(
        lambda obj: SearchParamsFactory.generate_sort_queries(
            obj.tableId, obj.create_sort
        )
        if obj.get_sort
        else []
    )
    filters: Any = LazyAttribute(
        lambda obj: [
            FilterQueryFactory(
                filter_for=dict([random.choice(list(obj.tableId.items()))]),
            )
            for _ in range(obj.create_filter)
        ]
        if obj.get_filter
        else []
    )

    sort_test_ids: Any = LazyAttribute(
        lambda x: ", ".join(f"{s.id}-{'desc' if s.desc else 'asc'}" for s in x.sort)
    )
