#!/usr/bin/python3

import random
from typing import Any
from factory import SubFactory, LazyAttribute, Iterator
from faker import Faker
from models.academic_term import AcademicTerm
from extension.enums.enum import AcademicTermEnum, AcademicTermTypeEnum
from models import storage
from .year_factory import YearFactory
from .base_factory import BaseFactory


fake = Faker()


class AcademicTermFactory(BaseFactory[AcademicTerm]):
    class Meta:
        model = AcademicTerm
        exclude = ("year",)

    year: Any = SubFactory(YearFactory)
    year_id: Any = LazyAttribute(lambda x: x.year.id)

    name: Any = Iterator(list(AcademicTermEnum._value2member_map_), cycle=True)

    start_date: Any = LazyAttribute(lambda x: fake.past_date())
    end_date: Any = LazyAttribute(lambda x: fake.future_date())

    registration_start: Any = LazyAttribute(lambda obj: fake.past_date())
    registration_end: Any = LazyAttribute(lambda obj: fake.future_date())

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Check if AcademicTerm exists
        existing = (
            storage.session.query(AcademicTerm)
            .filter_by(
                year_id=kwargs.get("year_id"),
                name=kwargs.get("name"),
            )
            .first()
        )
        if existing:
            return existing

        raise ValueError(
            "create necessary academic data before calling AcademicTermFactory"
        )
