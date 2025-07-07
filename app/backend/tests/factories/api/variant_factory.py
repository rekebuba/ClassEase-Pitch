import random
from typing import Any
from factory import LazyAttribute
from dataclasses import dataclass
from .typed_factory import TypedFactory

OPERATOR_CONFIG = {
    "text": ["iLike", "notLike", "startsWith", "endWith", "eq"],
    "number": ["eq", "ne", "lt", "lte", "gt", "gte"],
    "select": ["eq", "ne", "isEmpty", "isNotEmpty"],
    "multiSelect": ["in", "notIn", "isEmpty", "isNotEmpty"],
    "range": ["isBetween", "isNotBetween"],
    "date": [
        "eq",
        "ne",
        "lt",
        "lte",
        "gt",
        "gte",
        "isBetween",
        "isRelativeToToday",
        "isEmpty",
        "isNotEmpty",
    ],
    "dateRange": [
        "eq",
        "ne",
        "lt",
        "lte",
        "gt",
        "gte",
        "isBetween",
        "isRelativeToToday",
        "isEmpty",
        "isNotEmpty",
    ],
    "boolean": ["eq", "ne"],
}


@dataclass
class Variant:
    value: str

    def __post_init__(self):
        if self.value not in OPERATOR_CONFIG:
            raise ValueError(
                f"Invalid value '{self.value}'. Must be one of {list(OPERATOR_CONFIG)}"
            )


class variantFactory(TypedFactory[Variant]):
    class Meta:
        model = Variant
        exclude = ("variant_for", "variants")

    # general fields helping defining others
    variant_for: Any = LazyAttribute(lambda _: None)
    variants: Any = LazyAttribute(
        lambda _: {
            "identification": ["text"],
            "createdAt": ["dateRange"],
            "firstName_fatherName_grandFatherName": ["text"],
            "guardianName": ["text"],
            "guardianPhone": ["text"],
            "isActive": ["boolean"],
            "grade": ["multiSelect"],
            "sectionSemesterOne": ["multiSelect"],
            "sectionSemesterTwo": ["multiSelect"],
            "averageSemesterOne": ["multiSelect"],
            "averageSemesterTwo": ["multiSelect"],
            "rankSemesterOne": ["multiSelect"],
            "rankSemesterTwo": ["multiSelect"],
            "finalScore": ["multiSelect"],
            "rank": ["multiSelect"],
        }
    )
    value: Any = LazyAttribute(
        lambda obj: random.choice(obj.variants.get(obj.variant_for, []))
    )
