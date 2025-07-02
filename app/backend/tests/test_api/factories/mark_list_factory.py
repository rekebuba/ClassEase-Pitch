from typing import Any, Dict
from factory import LazyAttribute
import factory
from dataclasses import dataclass, asdict
from .mark_assessment_factory import MarkAssessmentFactory
from .default_felids import DefaultFelids


@dataclass
class FakeMarkList:
    grade_num: int  # number of mark List to create based on available grades
    academic_year: int
    semester: int
    mark_assessment: Dict[str, Any]

    def to_dict(self):
        return asdict(self)  # Converts all fields to dict automatically


class MarkListFactory(factory.Factory[Any]):
    class Meta:
        model = FakeMarkList

    academic_year: Any = LazyAttribute(lambda _: DefaultFelids.current_EC_year())
    semester: Any = LazyAttribute(lambda _: 1)
    grade_num: Any = LazyAttribute(lambda _: 0)  # number of available grades
    mark_assessment: Any = LazyAttribute(
        lambda obj: [MarkAssessmentFactory() for _ in range(obj.grade_num)]
    )
