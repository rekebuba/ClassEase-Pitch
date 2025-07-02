import random
from typing import Any
from factory import LazyAttribute, RelatedFactoryList
from models.section import Section
from models import storage
from .base_factory import BaseFactory


class SectionFactory(BaseFactory[Section]):
    class Meta:
        model = Section

    student_semester_records: Any = RelatedFactoryList(
        "tests.test_api.factories.StudentSemesterRecordFactory",
        factory_related_name="section",
        size=2,
    )

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
