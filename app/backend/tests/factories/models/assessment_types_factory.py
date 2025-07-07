import random
from typing import Any
from factory import LazyAttribute
import factory
from dataclasses import dataclass


@dataclass
class AssessmentTypes:
    type: str
    percentage: int


class AssessmentTypesFactory(factory.Factory[Any]):
    class Meta:
        model = AssessmentTypes

    type: Any = LazyAttribute(lambda _: random.choice(["Mid", "Final"]))
    percentage: Any = LazyAttribute(lambda obj: 30 if obj.type == "Mid" else 70)
