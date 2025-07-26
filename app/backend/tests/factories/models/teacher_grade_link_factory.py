from typing import Any
from factory import LazyAttribute, SubFactory
from faker import Faker

from models.teacher_grade_link import TeacherGradeLink
from .base_factory import BaseFactory


fake = Faker()


class TeacherGradeLinkFactory(BaseFactory[TeacherGradeLink]):
    class Meta:
        model = TeacherGradeLink
        exclude = ("teacher", "grade")

    teacher: Any = SubFactory(
        "tests.factories.models.teacher_factory.TeacherFactory", grades_to_teach=[]
    )
    grade: Any = SubFactory("tests.factories.models.grade_factory.GradeFactory")

    teacher_id: Any = LazyAttribute(lambda x: x.teacher.id if x.teacher else None)
    grade_id: Any = LazyAttribute(lambda x: x.grade.id if x.grade else None)
