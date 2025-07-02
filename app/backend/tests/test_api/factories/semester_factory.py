from typing import Any
import factory
from factory import SubFactory, LazyAttribute
from faker import Faker
from models.semester import Semester
from models import storage
from tests.test_api.factories.year_factory import YearFactory
from .base_factory import BaseFactory

fake = Faker()


class SemesterFactory(BaseFactory[Semester]):
    """Factory for creating Semester instances."""

    class Meta:
        model = Semester
        exclude = ("year",)

    year: Any = SubFactory(YearFactory, semesters=[])
    year_id: Any = LazyAttribute(lambda x: x.year.id)

    name: Any = factory.Sequence(
        lambda n: 1 if n % 2 == 0 else 2
    )  # Alternates between 1 and 2

    start_date: Any = LazyAttribute(lambda x: fake.past_date())
    end_date: Any = LazyAttribute(lambda x: fake.future_date())

    registration_start: Any = LazyAttribute(lambda obj: fake.past_date())
    registration_end: Any = LazyAttribute(lambda obj: fake.future_date())

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Check if semester
        existing = (
            storage.session.query(Semester)
            .filter_by(year_id=kwargs.get("year_id"), name=kwargs.get("name"))
            .first()
        )
        return existing or super()._create(model_class, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        name = kwargs.get("name", self.name)
        if name not in [1, 2]:
            raise ValueError(f"Invalid semester name: {name}. Only 1 or 2 are allowed.")

        # check if semester 1 was created before creating semester 2
        if name == 2:
            semester_1 = SemesterFactory.get(name=1)
            if semester_1 is None:
                raise ValueError("Semester 1 must be created before Semester 2.")

        # Call the parent constructor
        super().__init__(*args, **kwargs)
