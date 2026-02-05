from typing import (
    Any,
    Generic,
    Optional,
    Type,
    TypeVar,
)

from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy.orm import Session, scoped_session

T = TypeVar("T")


class BaseFactory(SQLAlchemyModelFactory, Generic[T]):
    """Base factory class for creating database models."""

    class Meta:
        abstract = True

    @classmethod
    def get_or_create(cls: Type["BaseFactory[T]"], **kwargs: Any) -> T:
        model = getattr(cls._meta, "model", None)
        session: Optional[scoped_session[Session]] = getattr(
            cls._meta, "sqlalchemy_session", None
        )
        if model is None or session is None:
            raise ValueError(
                "Model and session must be defined in the factory's Meta class."
            )

        lookup_kwargs = {k: v for k, v in kwargs.items()}

        existing = session.query(model).filter_by(**lookup_kwargs).first()
        if existing:
            return existing

        return cls.create(**kwargs)

    @classmethod
    def get(
        cls: Type["BaseFactory[T]"], **kwargs: Any
    ) -> Optional[scoped_session[Session]]:
        model = getattr(cls._meta, "model", None)
        session: Optional[Session] = getattr(cls._meta, "sqlalchemy_session", None)
        if model is None or session is None:
            raise ValueError(
                "Model and session must be defined in the factory's Meta class."
            )

        lookup_kwargs = {k: v for k, v in kwargs.items()}

        existing = session.query(model).filter_by(**lookup_kwargs).first()
        if existing:
            return existing

        return None

    @classmethod
    def _create(
        cls: Type["BaseFactory[T]"], model_class: Type[T], *arg: Any, **kwargs: Any
    ) -> T:
        """
        Override creation to add specific fields marked in _add_for_session
        """
        add_fields = getattr(cls, "_add_for_session", {})

        # Add to attributes
        for field, value in add_fields.items():
            all_args = field.split(".")
            key = all_args[0]
            args = {}
            for v in all_args[1:]:
                args[v] = kwargs.get(v, None)
            kwargs[key] = value(**args)

        # Skip fields that are not needed for the session
        skip_fields = getattr(cls, "_skip_fields", [])
        for k in skip_fields:
            kwargs.pop(k, None)

        return super()._create(model_class, *arg, **kwargs)

    @classmethod
    def create(cls: Type["BaseFactory[T]"], **kwargs: Any) -> T:
        return super().create(**kwargs)
