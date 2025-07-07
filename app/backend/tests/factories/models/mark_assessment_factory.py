import random
from typing import Any, List
from factory import LazyAttribute
import factory
from dataclasses import dataclass
from .subjects_factory import SubjectsFactory
from .assessment_types_factory import AssessmentTypesFactory


@dataclass
class MarkAssessment:
    grade: int
    subjects: List[Any]
    assessment_type: List[Any]


class MarkAssessmentFactory(factory.Factory[Any]):
    class Meta:
        model = MarkAssessment

    grade: Any = LazyAttribute(lambda _: random.randint(1, 10))
    subjects: Any = LazyAttribute(lambda _: SubjectsFactory.create_batch(4))
    assessment_type: Any = LazyAttribute(
        lambda _: AssessmentTypesFactory.create_batch(2)
    )
