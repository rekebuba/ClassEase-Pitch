from typing import (
    Any,
    Generic,
    TypeVar,
)

import factory

T = TypeVar("T")


class TypedFactory(factory.Factory, Generic[T]):  # type: ignore[type-arg]
    class Meta:
        model = None  # Placeholder, set in subclasses

    @classmethod
    def build(cls, **kwargs: Any) -> T:
        return super().build(**kwargs)  # type: ignore[no-any-return]

    @classmethod
    def create(cls, **kwargs: Any) -> T:
        return super().create(**kwargs)  # type: ignore[no-any-return]
