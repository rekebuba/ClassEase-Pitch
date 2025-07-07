import random
from typing import Any
from extension.enums.enum import StreamEnum
from models import storage
from models.stream import Stream
from factory import LazyAttribute
from .base_factory import BaseFactory


class StreamFactory(BaseFactory[Stream]):
    """Factory for creating Stream instances."""

    class Meta:
        model = Stream

    name: Any = LazyAttribute(
        lambda x: random.choice(list(StreamEnum._value2member_map_))
    )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Check if stream with the same name already exists
        existing = storage.session.query(Stream).filter_by(**kwargs).first()
        return existing or super()._create(model_class, *args, **kwargs)
