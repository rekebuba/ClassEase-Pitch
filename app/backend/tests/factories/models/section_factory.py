import random
from typing import Any
from factory import LazyAttribute, RelatedFactoryList, SubFactory
from models.section import Section
from models import storage
from .base_factory import BaseFactory


class SectionFactory(BaseFactory[Section]):
    class Meta:
        model = Section
        exclude = ("year",)

    year: Any = SubFactory("tests.factories.models.YearFactory")

    student_term_records: Any = RelatedFactoryList(
        "tests.factories.models.StudentTermRecordFactory",
        factory_related_name="section",
        size=2,
    )

    year_id: Any = LazyAttribute(lambda x: x.year.id)
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
