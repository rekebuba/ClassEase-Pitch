from typing import Any
from factory import LazyAttribute, SubFactory
from faker import Faker

from models.teacher_section_link import TeacherSectionLink
from .base_factory import BaseFactory


fake = Faker()


class TeacherSectionLinkFactory(BaseFactory[TeacherSectionLink]):
    class Meta:
        model = TeacherSectionLink
        exclude = ("teacher", "section")

    teacher: Any = SubFactory("tests.factories.models.teacher_factory.TeacherFactory")
    section: Any = SubFactory("tests.factories.models.section_factory.SectionFactory")

    teacher_id: Any = LazyAttribute(lambda x: x.teacher.id)
    section_id: Any = LazyAttribute(lambda x: x.section.id)
