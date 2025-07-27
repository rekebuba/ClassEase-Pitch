import random
from typing import Any
from factory import LazyAttribute, RelatedFactoryList, SubFactory
from models.section import Section
from models import storage
from .base_factory import BaseFactory


class SectionFactory(BaseFactory[Section]):
    class Meta:
        model = Section
        exclude = ("grade",)

    grade: Any = SubFactory("tests.factories.models.GradeFactory")

    grade_id: Any = LazyAttribute(lambda x: x.grade.id)
    section: Any = LazyAttribute(lambda _: random.choice(["A", "B", "C"]))

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        check if section already exists
        """
        existing = storage.session.query(Section).filter_by(**kwargs).first()
        if existing:
            return existing
        return super()._create(model_class, *args, **kwargs)
