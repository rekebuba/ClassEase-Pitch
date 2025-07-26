from typing import Any
from factory import LazyAttribute, SubFactory
from faker import Faker

from models.student_grade_link import StudentGradeLink
from .base_factory import BaseFactory


fake = Faker()


class StudentGradeLinkFactory(BaseFactory[StudentGradeLink]):
    class Meta:
        model = StudentGradeLink
        exclude = ("student", "grade")

    student: Any = SubFactory("tests.factories.models.student_factory.StudentFactory", grades=[])
    grade: Any = SubFactory("tests.factories.models.grade_factory.GradeFactory")

    student_id: Any = LazyAttribute(lambda x: x.student.id if x.student else None)
    grade_id: Any = LazyAttribute(lambda x: x.grade.id if x.grade else None)
