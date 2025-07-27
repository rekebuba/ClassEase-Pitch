from typing import Any
from factory import LazyAttribute, SubFactory
from faker import Faker
from models.teacher_year_link import TeacherYearLink
from .base_factory import BaseFactory


fake = Faker()


class TeacherYearLinkFactory(BaseFactory[TeacherYearLink]):
    class Meta:
        model = TeacherYearLink
        exclude = ("teacher", "year")

    teacher: Any = SubFactory(
        "tests.factories.models.teacher_factory.TeacherFactory", years=[]
    )
    year: Any = SubFactory("tests.factories.models.year_factory.YearFactory")

    teacher_id: Any = LazyAttribute(lambda x: x.teacher.id if x.teacher else None)
    year_id: Any = LazyAttribute(lambda x: x.year.id if x.year else None)
