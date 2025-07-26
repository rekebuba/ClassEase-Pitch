from typing import Any
from factory import LazyAttribute, SubFactory
from faker import Faker

from models.student_section_link import StudentSectionLink
from .base_factory import BaseFactory


fake = Faker()


class StudentSectionLinkFactory(BaseFactory[StudentSectionLink]):
    class Meta:
        model = StudentSectionLink
        exclude = ("student", "section")

    student: Any = SubFactory("tests.factories.models.student_factory.StudentFactory")
    section: Any = SubFactory(
        "tests.factories.models.section_factory.SectionFactory", student_term_records=[]
    )

    student_id: Any = LazyAttribute(lambda x: x.student.id if x.student else None)
    section_id: Any = LazyAttribute(lambda x: x.section.id if x.section else None)
