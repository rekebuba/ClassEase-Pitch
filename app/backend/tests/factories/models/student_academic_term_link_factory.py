from typing import Any
from factory import LazyAttribute, SubFactory
from faker import Faker

from models.student_academic_term_link import StudentAcademicTermLink
from .base_factory import BaseFactory


fake = Faker()


class StudentAcademicTermLinkFactory(BaseFactory[StudentAcademicTermLink]):
    class Meta:
        model = StudentAcademicTermLink
        exclude = ("student", "academic_term")

    student: Any = SubFactory(
        "tests.factories.models.student_factory.StudentFactory", academic_terms=[]
    )
    academic_term: Any = SubFactory(
        "tests.factories.models.academic_term_factory.AcademicTermFactory"
    )

    student_id: Any = LazyAttribute(lambda x: x.student.id if x.student else None)
    academic_term_id: Any = LazyAttribute(
        lambda x: x.academic_term.id if x.academic_term else None
    )

    average = None
    rank = None
