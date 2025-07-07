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

    name: Any = LazyAttribute(
        lambda _: random.choice(list(AllSubjectsEnum._value2member_map_))
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

    @classmethod
    def get_existing_id(cls, student_grade_id: str, offset: int) -> str:
        """
        Returns an existing subject ID if available, otherwise raise ValueError.
        """
        stmt = (
            select(Subject.id)
            .join(Grade)
            .where(Grade.id == student_grade_id)
            .order_by(Subject.id)
            .offset(offset)
            .limit(1)
        )

        result = storage.session.scalars(stmt).first()  # returns single value or None

        if result is None:
            raise ValueError(
                f"No subject found for grade ID {student_grade_id} at offset {offset}"
            )

        return result
