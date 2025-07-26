from typing import Any
from factory import LazyAttribute, SubFactory
from faker import Faker

from models.student_subject_link import StudentSubjectLink
from .base_factory import BaseFactory


fake = Faker()


class StudentSubjectLinkFactory(BaseFactory[StudentSubjectLink]):
    class Meta:
        model = StudentSubjectLink
        exclude = ("student", "subject")

    student: Any = SubFactory("tests.factories.models.student_factory.StudentFactory")
    subject: Any = SubFactory("tests.factories.models.subject_factory.SubjectFactory")

    student_id: Any = LazyAttribute(lambda x: x.student.id if x.student else None)
    subject_id: Any = LazyAttribute(lambda x: x.subject.id if x.subject else None)
