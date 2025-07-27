from typing import Any
from factory import LazyAttribute, SubFactory
from faker import Faker

from models.teacher_subject_link import TeacherSubjectLink
from .base_factory import BaseFactory


fake = Faker()


class TeacherSubjectLinkFactory(BaseFactory[TeacherSubjectLink]):
    class Meta:
        model = TeacherSubjectLink
        exclude = ("teacher", "subject")

    teacher: Any = SubFactory(
        "tests.factories.models.teacher_factory.TeacherFactory", subjects=[]
    )
    subject: Any = SubFactory("tests.factories.models.subject_factory.SubjectFactory")

    teacher_id: Any = LazyAttribute(lambda x: x.teacher.id if x.teacher else None)
    subject_id: Any = LazyAttribute(lambda x: x.subject.id if x.subject else None)
