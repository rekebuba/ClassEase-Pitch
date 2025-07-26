import random
from typing import Any
from factory import LazyAttribute, SubFactory

from extension.enums.enum import MarkListTypeEnum
from models.mark_list import MarkList
from tests.factories.models.base_factory import BaseFactory


class MarkListFactory(BaseFactory[MarkList]):
    class Meta:
        model = MarkList
        exclude = ("student", "academic_term", "subject")

    student: Any = SubFactory("tests.factories.models.student_factory.StudentFactory")
    academic_term: Any = SubFactory(
        "tests.factories.models.academic_term_factory.AcademicTermFactory"
    )
    subject: Any = SubFactory("tests.factories.models.subject_factory.SubjectFactory")

    # fields will be assigned on call
    student_id: Any = LazyAttribute(lambda x: x.student.id)
    subject_id: Any = LazyAttribute(lambda x: x.subject.id)
    academic_term_id: Any = LazyAttribute(lambda x: x.academic_term.id)

    type: Any = LazyAttribute(
        lambda x: random.choice(list(MarkListTypeEnum._value2member_map_))
    )
    percentage: Any = LazyAttribute(lambda x: random.choice([10, 20, 50, 100]))
    score: Any = None
