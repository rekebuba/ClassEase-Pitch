import random
from typing import Any
from factory import LazyAttribute, SubFactory, SelfAttribute
import factory

from extension.enums.enum import MarkListTypeEnum
from models.mark_list import MarkList


class MarkListFactory(factory.Factory[Any]):
    class Meta:
        model = MarkList

    student: Any = SubFactory("tests.test_api.factories.StudentFactory")
    student_term_record: Any = SubFactory(
        "tests.test_api.factories.StudentTermRecordFactory",
        student=SelfAttribute("..student"),
        assessments=[],
    )
    yearly_subject: Any = SubFactory("tests.test_api.factories.YearlySubjectFactory")

    student_id: Any = LazyAttribute(lambda x: x.student.id)
    student_term_record_id: Any = LazyAttribute(lambda x: x.student_term_record.id)
    yearly_subject_id: Any = LazyAttribute(lambda x: x.yearly_subject.id)

    type: Any = LazyAttribute(
        lambda x: random.choice(list(MarkListTypeEnum._value2member_map_))
    )
    percentage: Any = LazyAttribute(lambda x: random.choice([10, 20, 50, 100]))
    score: Any = LazyAttribute(lambda x: random.uniform(10, 100))
