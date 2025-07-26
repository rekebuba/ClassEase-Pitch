from typing import Any
from factory import LazyAttribute, SubFactory
from faker import Faker

from models.student_stream_link import StudentStreamLink
from .base_factory import BaseFactory


fake = Faker()


class StudentStreamLinkFactory(BaseFactory[StudentStreamLink]):
    class Meta:
        model = StudentStreamLink
        exclude = ("student", "stream")

    student: Any = SubFactory(
        "tests.factories.models.student_factory.StudentFactory", streams=[]
    )
    stream: Any = SubFactory("tests.factories.models.stream_factory.StreamFactory")

    student_id: Any = LazyAttribute(lambda x: x.student.id if x.student else None)
    stream_id: Any = LazyAttribute(lambda x: x.stream.id if x.stream else None)
