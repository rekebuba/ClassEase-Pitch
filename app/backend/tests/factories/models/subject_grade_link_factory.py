from typing import Any
from factory import LazyAttribute, SubFactory
from faker import Faker

from models.subject_grade_link import SubjectGradeLink
from .base_factory import BaseFactory
from models import storage


fake = Faker()


class SubjectGradeLinkFactory(BaseFactory[SubjectGradeLink]):
    class Meta:
        model = SubjectGradeLink
        exclude = ("subject", "grade")

    subject: Any = SubFactory("tests.factories.models.subject_factory.SubjectFactory")
    grade: Any = SubFactory("tests.factories.models.grade_factory.GradeFactory")

    subject_id: Any = LazyAttribute(lambda x: x.subject.id if x.subject else None)
    grade_id: Any = LazyAttribute(lambda x: x.grade.id if x.grade else None)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Try to get existing link first
        existing = storage.session.query(SubjectGradeLink).filter_by(**kwargs).first()
        return existing or super()._create(model_class, *args, **kwargs)
