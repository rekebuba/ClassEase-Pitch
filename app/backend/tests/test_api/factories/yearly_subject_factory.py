import json
from typing import Any

from models.yearly_subject import YearlySubject
from .base_factory import BaseFactory
from factory import LazyAttribute, SubFactory, RelatedFactoryList, SelfAttribute
from models import storage


class YearlySubjectFactory(BaseFactory[YearlySubject]):
    """Factory for creating YearlySubject instances in the database."""

    class Meta:
        model = YearlySubject
        exclude = ("year", "subject", "grade", "stream")

    year: Any = SubFactory("tests.test_api.factories.YearFactory")
    subject: Any = SubFactory("tests.test_api.factories.SubjectFactory")
    grade: Any = SubFactory("tests.test_api.factories.GradeFactory")
    stream: Any = SubFactory("tests.test_api.factories.StreamFactory")

    year_id: Any = LazyAttribute(lambda x: x.year.id)
    subject_id: Any = LazyAttribute(lambda x: x.subject.id)
    grade_id: Any = LazyAttribute(lambda x: x.grade.id)
    stream_id: Any = LazyAttribute(
        lambda x: x.stream.id if x.grade.grade in ["11", "12"] else None
    )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Check if yearly subject with the same year, subject, grade, and stream already exists
        existing = (
            storage.session.query(YearlySubject)
            .filter_by(
                year_id=kwargs.get("year_id"),
                subject_id=kwargs.get("subject_id"),
            )
            .first()
        )
        return existing or super()._create(model_class, *args, **kwargs)
