import random
from typing import Any
from factory import LazyAttribute, RelatedFactoryList
from sqlalchemy import select
from extension.enums.enum import AllSubjectsEnum
from models.subject import Subject
from models.grade import Grade
from models import storage
from .base_factory import BaseFactory


class SubjectFactory(BaseFactory[Subject]):
    class Meta:
        model = Subject
        exclude = ("words", "prefix_length")

    words: Any = LazyAttribute(lambda x: x.name.split())
    prefix_length = 3

    name: Any = LazyAttribute(
        lambda _: random.choice(list(AllSubjectsEnum._value2member_map_))
    )
    code: Any = LazyAttribute(
        lambda x: "".join(
            [
                word[: x.prefix_length].upper()
                for word in x.words
                if word.isalpha() and word != "and"
            ]
        )
    )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Override the _create method to check for existing subjects.
        If a subject with the same name exists, return it instead of creating a new one.
        """
        existing = (
            storage.session.query(Subject).filter_by(name=kwargs.get("name")).first()
        )
        return existing or super()._create(model_class, *args, **kwargs)
