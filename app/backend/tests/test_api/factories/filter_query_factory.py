import random
from typing import Any
from factory import LazyAttribute
from dataclasses import dataclass
from .typed_factory import TypedFactory
from .variant_factory import variantFactory, OPERATOR_CONFIG
from .value_factory import valueFactory


@dataclass
class FilterQuery:
    id: str
    tableId: str
    variant: str
    operator: str
    value: Any


class FilterQueryFactory(TypedFactory[FilterQuery]):
    class Meta:
        model = FilterQuery
        exclude = ("filter_for",)

    # general fields helping defining others
    filter_for: Any = LazyAttribute(lambda _: None)

    id: Any = LazyAttribute(lambda x: next(iter(x.filter_for.items()))[0])
    tableId: Any = LazyAttribute(lambda x: next(iter(x.filter_for.items()))[1])
    variant: Any = LazyAttribute(lambda x: variantFactory(variant_for=x.id).value)
    operator: Any = LazyAttribute(
        lambda x: random.choice(OPERATOR_CONFIG.get(x.variant, []))
    )

    value: Any = LazyAttribute(lambda x: getattr(valueFactory(), x.id))

    def __init__(self, *args: Any, **kwargs: Any) -> Any:
        filter_for = kwargs.get("filter_for", self.filter_for)
        if not filter_for:
            raise ValueError("filter_for is required and cannot be None")

        # Call the parent constructor
        super().__init__(*args, **kwargs)
