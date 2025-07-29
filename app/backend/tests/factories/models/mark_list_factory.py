from itertools import cycle
import random
from typing import Any
from factory import LazyAttribute, SubFactory, LazyFunction

from extension.enums.enum import MarkListTypeEnum
from models.mark_list import MarkList
from tests.factories.models.base_factory import BaseFactory


class MarkListFactory(BaseFactory[MarkList]):
    class Meta:
        model = MarkList
        exclude = ("student", "academic_term", "subject")

    student: Any = SubFactory("tests.factories.models.student_factory.StudentFactory")
    student_term_record: Any = SubFactory(
        "tests.factories.models.student_term_record_factory.StudentTermRecordFactory"
    )
    subject: Any = SubFactory("tests.factories.models.subject_factory.SubjectFactory")

    # fields will be assigned on call
    student_id: Any = LazyAttribute(lambda x: x.student.id)
    subject_id: Any = LazyAttribute(lambda x: x.subject.id)
    student_term_record_id: Any = LazyAttribute(lambda x: x.student_term_record.id)

    type: Any = LazyFunction(
        lambda: next(cycle(MarkListTypeEnum._value2member_map_.values()))
    )
    percentage: Any = LazyFunction(lambda: next(cycle([10, 5, 5, 30, 50])))
    score: Any = None
