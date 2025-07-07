from typing import Any, List, Optional
import random
from factory import LazyAttribute
from dataclasses import dataclass
from .typed_factory import TypedFactory
from .search_params_factory import SearchParams, SearchParamsFactory


@dataclass
class QueryResponse:
    columns: List[str]
    search_params: SearchParams
    table_name: Optional[str] = None


class QueryFactory(TypedFactory[QueryResponse]):
    class Meta:
        model = QueryResponse
        exclude = ("tableId",)

    # general fields helping defining others
    tableId: Any = LazyAttribute(lambda _: None)

    table_name: Any = LazyAttribute(lambda _: "students")
    columns: Any = LazyAttribute(
        lambda obj: random.sample(
            list(obj.tableId.keys()), random.randint(1, len(obj.tableId))
        )
    )
    search_params: Any = LazyAttribute(
        lambda obj: SearchParamsFactory.create(tableId=obj.tableId)
    )

    def __init__(self, *args: Any, **kwargs: Any) -> Any:
        tableId = kwargs.get("tableId", self.tableId)
        if not tableId:
            raise ValueError("tableId is required and cannot be None")

        # Call the parent constructor
        super().__init__(*args, **kwargs)
