import random
from typing import Any
from factory import LazyAttribute, SubFactory, SelfAttribute
import factory

from extension.enums.enum import MarkListTypeEnum
from models.mark_list import MarkList


class MarkListFactory(factory.Factory[Any]):
    class Meta:
        model = MarkList

    # fields will be assigned on call
    student_id: Any = None
    academic_term_id: Any = None
    yearly_subject_id: Any = None

    type: Any = LazyAttribute(
        lambda x: random.choice(list(MarkListTypeEnum._value2member_map_))
    )
    percentage: Any = LazyAttribute(lambda x: random.choice([10, 20, 50, 100]))
    score: Any = LazyAttribute(lambda x: random.uniform(10, 100))
