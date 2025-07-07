from typing import Any
from factory import LazyAttribute
import factory
from dataclasses import dataclass


@dataclass(kw_only=True)
class AvailableSubject:
    grade: int
    subject: str
    subject_code: str


class SubjectsFactory(factory.Factory[Any]):
    class Meta:
        model = AvailableSubject

    subject: Any = LazyAttribute(lambda _: None)
    subject_code: Any = LazyAttribute(lambda _: None)
    grade: Any = LazyAttribute(lambda _: None)
