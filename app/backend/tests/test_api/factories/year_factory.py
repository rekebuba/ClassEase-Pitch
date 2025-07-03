#!/usr/bin/python3
"""Module for YearFactory class"""

import random
from typing import Any
from factory import LazyAttribute
from extension.enums.enum import AcademicTermTypeEnum
from models.year import Year
from models import storage
from .base_action import BaseAction
from .base_factory import BaseFactory
from extension.functions.helper import academic_year, current_EC_year, current_GC_year


class YearFactory(BaseFactory[Year]):
    """Factory for creating Year instances in the database."""

    class Meta:
        model = Year

    # calendar_type: Any = LazyAttribute(
    #     lambda _: random.choice(list(AcademicTermTypeEnum._value2member_map_))
    # )
    calendar_type: Any = LazyAttribute(lambda _: AcademicTermTypeEnum.QUARTER.value)

    ethiopian_year: Any = LazyAttribute(lambda _: current_EC_year())
    gregorian_year: Any = LazyAttribute(lambda x: current_GC_year(x.ethiopian_year))
    academic_year: Any = LazyAttribute(lambda x: academic_year(x.ethiopian_year))

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Try to get existing year first
        existing = (
            storage.session.query(Year)
            .filter_by(academic_year=kwargs.get("academic_year"))
            .first()
        )
        if existing:
            return existing

        # Create the year instance
        year = super()._create(model_class, *args, **kwargs)

        # Populate subjects and yearly_subjects
        BaseAction.create_necessary_academic_data(year)

        return year
