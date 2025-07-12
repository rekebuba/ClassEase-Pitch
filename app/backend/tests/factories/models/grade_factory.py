import random
from typing import Any, Optional
from factory import LazyAttribute, SubFactory
from sqlalchemy import select
from models.grade import Grade
from models import storage
from .base_factory import BaseFactory
from extension.enums.enum import GradeLevelEnum


class GradeFactory(BaseFactory[Grade]):
    class Meta:
        model = Grade
        exclude = "year"

    # preload IDs
    _existing_ids = storage.session.execute(select(Grade.grade, Grade.id)).all()
    year: Any = SubFactory("tests.factories.models.year_factory.YearFactory")

    year_id: Any = LazyAttribute(lambda x: x.year.id)
    grade: Any = LazyAttribute(lambda _: str(random.choice(range(1, 13))))
    level: Any = LazyAttribute(
        lambda x: GradeLevelEnum.PRIMARY.value
        if int(x.grade) < 5
        else GradeLevelEnum.MIDDLE_SCHOOL.value
        if int(x.grade) < 8
        else GradeLevelEnum.HIGH_SCHOOL.value
    )
    has_stream: Any = LazyAttribute(
        lambda x: True if x.grade in ["11", "12"] else False
    )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Try to get existing user first
        existing = storage.session.query(Grade).filter_by(**kwargs).first()
        return existing or super()._create(model_class, *args, **kwargs)

    @classmethod
    def get_existing_id(cls, grade: int) -> Optional[str]:
        """
        Returns an existing grade ID if available, otherwise None.
        """
        for existing_grade, existing_id in cls._existing_ids:
            if existing_grade == grade:
                return str(existing_id) if existing_id is not None else None
        # If no matching grade found, return None
        return None

    @classmethod
    def get_grade(cls, grade: int) -> Optional[Grade]:
        """
        Returns a Grade instance for the given grade number if it exists.
        """
        existing_id = cls.get_existing_id(grade)
        if existing_id:
            return storage.session.get(Grade, existing_id)
        return None
