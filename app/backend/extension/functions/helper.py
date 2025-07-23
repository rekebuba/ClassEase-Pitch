from typing import Any, Type, List, Union, get_origin, get_args, Annotated
from datetime import datetime
import re
from pyethiodate import EthDate  # type: ignore
from pydantic import BaseModel


def to_camel(string: str) -> str:
    """Alias generator to convert snake_case → camelCase"""
    parts = string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


def to_snake(s: str) -> str:
    # Replace dashes with underscores
    s = s.replace("-", "_")

    # Insert underscore before capital letters (except the first one)
    s = re.sub(r"(?<!^)(?=[A-Z])", "_", s)

    return s.lower()


def current_EC_year() -> EthDate:
    return EthDate.date_to_ethiopian(datetime.now()).year


def current_GC_year(ethiopian_year: int) -> str:
    return f"{ethiopian_year + 7}-{ethiopian_year + 8}"


def academic_year(ethiopian_year: int) -> str:
    gregorian_year = current_GC_year(ethiopian_year)
    return f"{ethiopian_year} E.C/{gregorian_year} G.C"


def extract_inner_model(annotation: Any) -> Type[BaseModel]:
    """
    Extract the inner Pydantic model class from a possibly nested type annotation.
    Raises ValueError if the annotation doesn't resolve to a BaseModel subclass.

    Handles:
    - List[Model]
    - Optional[List[Model]] or Union[List[Model], None]
    - Annotated[List[Model], ...]
    - Direct Model reference
    """
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union/Optional (Optional[T] is just Union[T, None])
    if origin is Union:
        non_none_args = [arg for arg in args if arg is not type(None)]
        if non_none_args:
            return extract_inner_model(non_none_args[0])

    # Handle List types
    if origin in (list, List):
        return extract_inner_model(args[0])

    # Handle Annotated types
    if origin is Annotated:
        return extract_inner_model(args[0])

    # Base case - must be a BaseModel subclass
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return annotation

    raise ValueError(
        f"Type annotation does not resolve to a Pydantic model. "
        f"Got {annotation} which is not a BaseModel subclass."
    )
