from typing import Any, Optional
from factory import LazyAttribute, RelatedFactoryList
from sqlalchemy import select
from models.year import Year
from models import storage
from .base_action import BaseAction
from .base_factory import BaseFactory
from extension.functions.helper import academic_year, current_EC_year, current_GC_year


class YearFactory(BaseFactory[Year]):
    """Factory for creating Year instances in the database."""

    class Meta:
        model = Year

    semesters: Any = RelatedFactoryList(
        "tests.test_api.factories.SemesterFactory",
        factory_related_name="year",
        size=2,
    )  # Two semesters per year

    # Preload existing school IDs
    _existing_ids = storage.session.execute(select(Year.id)).scalar_one_or_none()

    ethiopian_year: Any = LazyAttribute(lambda _: current_EC_year())
    gregorian_year: Any = LazyAttribute(lambda x: current_GC_year(x.ethiopian_year))
    academic_year: Any = LazyAttribute(lambda x: academic_year(x.ethiopian_year))

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Try to get existing year first
        existing = storage.session.query(Year).filter_by(**kwargs).first()
        if existing:
            return existing

        # Create the year instance
        year = super()._create(model_class, *args, **kwargs)

        # Populate subjects and yearly_subjects
        BaseAction.create_necessary_academic_data(year)

        return year

    @classmethod
    def get_existing_id(cls) -> Optional[str]:
        return cls._existing_ids if cls._existing_ids else None

    @classmethod
    def get_year(cls, academic_year: str) -> Optional[Year]:
        """
        Returns a Year instance for the given year if it exists.
        """
        return storage.session.scalars(
            select(Year).where(Year.academic_year == academic_year)
        ).first()
