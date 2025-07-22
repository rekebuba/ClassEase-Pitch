from typing import Any
from factory import LazyAttribute, SubFactory
from faker import Faker
from models.student_year_link import StudentYearLink
from .base_factory import BaseFactory


fake = Faker()


class StudentYearLinkFactory(BaseFactory[StudentYearLink]):
    class Meta:
        model = StudentYearLink
        exclude = ("student", "year")

    student: Any = SubFactory("tests.factories.models.student_factory.StudentFactory")
    year: Any = SubFactory("tests.factories.models.year_factory.YearFactory")

    student_id: Any = LazyAttribute(lambda x: x.student.id if x.student else None)
    year_id: Any = LazyAttribute(lambda x: x.year.id if x.year else None)

    average = None
    rank = None
