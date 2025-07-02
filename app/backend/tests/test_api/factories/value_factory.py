import random
from typing import Any
from factory import LazyAttribute
from faker import Faker
from .typed_factory import TypedFactory
from .min_max_factory import MinMaxFactory
from datetime import date

fake = Faker()


class Value:
    identification: str
    createdAt: str
    firstName_fatherName_grandFatherName: str
    guardianName: str
    guardianPhone: str
    isActive: str
    grade: str
    sectionSemesterOne: str
    sectionSemesterTwo: str
    averageSemesterOne: str
    averageSemesterTwo: str
    rankSemesterOne: str
    rankSemesterTwo: str
    finalScore: str
    rank: str


class valueFactory(TypedFactory[Value]):
    class Meta:
        model = Value

    identification: Any = LazyAttribute(lambda _: "MAS/100/23")
    firstName_fatherName_grandFatherName: Any = LazyAttribute(lambda _: fake.name())
    guardianName: Any = LazyAttribute(lambda _: fake.name())
    guardianPhone: Any = LazyAttribute(lambda _: "091234567")
    isActive: Any = LazyAttribute(lambda _: fake.boolean())
    grade: Any = LazyAttribute(
        lambda _: random.sample(range(1, 11), random.randint(1, 10))
    )
    sectionSemesterOne: Any = LazyAttribute(
        lambda _: random.sample(["A", "B", "C"], random.randint(1, 3))
    )
    sectionSemesterTwo: Any = LazyAttribute(
        lambda _: random.sample(["A", "B", "C"], random.randint(1, 3))
    )
    createdAt: Any = LazyAttribute(
        lambda _: MinMaxFactory(
            type=date, lowest=fake.past_date(), highest=fake.future_date()
        )
    )
    averageSemesterOne: Any = LazyAttribute(lambda _: MinMaxFactory(type=float))
    averageSemesterTwo: Any = LazyAttribute(lambda _: MinMaxFactory(type=float))
    rankSemesterOne: Any = LazyAttribute(
        lambda _: MinMaxFactory(type=int, lowest=1, highest=3)
    )
    rankSemesterTwo: Any = LazyAttribute(
        lambda _: MinMaxFactory(type=int, lowest=1, highest=3)
    )
    finalScore: Any = LazyAttribute(lambda _: MinMaxFactory(type=float))
    rank: Any = LazyAttribute(lambda _: MinMaxFactory(type=int, lowest=1, highest=3))
