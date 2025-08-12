from typing import (
    Any,
    Tuple,
    Type,
    List,
    TypedDict,
    Union,
    get_origin,
    get_args,
    Annotated,
)
from datetime import date, datetime
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


def current_EC_year(date: date | datetime = datetime.now()) -> EthDate:
    return EthDate.date_to_ethiopian(date).year


def current_GC_year(ethiopian_year: int) -> str:
    return f"{ethiopian_year + 7}-{ethiopian_year + 8}"


def academic_year(ethiopian_year: int) -> str:
    gregorian_year = current_GC_year(ethiopian_year)
    return f"{ethiopian_year} E.C/{gregorian_year} G.C"


def extract_inner_model(annotation: Any) -> Tuple[bool, Type[BaseModel]]:
    """
    Extract the inner Pydantic model class from a possibly nested type annotation.
    Returns a tuple (is_list, model) where:
    - is_list: bool indicating if the original annotation was a List type
    - model: the extracted BaseModel subclass

    Raises ValueError if the annotation doesn't resolve to a BaseModel subclass.

    Handles:
    - List[Model] → (True, Model)
    - Optional[List[Model]] → (True, Model)
    - Optional[Model] → (False, Model)
    - Annotated[List[Model], ...] → (True, Model)
    - Direct Model reference → (False, Model)
    """
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union/Optional (Optional[T] is just Union[T, None])
    if origin is Union:
        non_none_args = [arg for arg in args if arg is not type(None)]
        if non_none_args:
            return extract_inner_model(non_none_args[0])

    # Handle List types - return True for is_list
    if origin in (list, List):
        is_list, model = extract_inner_model(args[0])
        return (True, model)

    # Handle Annotated types
    if origin is Annotated:
        return extract_inner_model(args[0])

    # Base case - must be a BaseModel subclass
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return (False, annotation)

    raise ValueError(
        f"Type annotation does not resolve to a Pydantic model. "
        f"Got {annotation} which is not a BaseModel subclass."
    )


class ModelClassification(TypedDict):
    model_class: List[str]
    model_sub_class: List[str]


def classify_model_fields(model: Type[BaseModel]) -> ModelClassification:
    """
    Analyze a Pydantic model and classify its fields into:
    - model_class: List of field names that are BaseModel subclasses
    - model_sub_class: List of field names that are not BaseModel subclasses

    Returns a dictionary with these two keys containing lists of field names.
    """
    result: ModelClassification = {"model_class": [], "model_sub_class": []}

    # Handle Pydantic v2 models
    if hasattr(model, "model_fields"):
        for field_name, field_info in model.model_fields.items():
            annotation = field_info.annotation

            try:
                _, model_type = extract_inner_model(annotation)
                if isinstance(model_type, type) and issubclass(model_type, BaseModel):
                    result["model_sub_class"].append(field_name)
                else:
                    result["model_class"].append(field_name)
            except ValueError:
                result["model_class"].append(field_name)
    # Fallback to __annotations__ for other cases
    elif hasattr(model, "__annotations__"):
        for field_name, annotation in model.__annotations__.items():
            try:
                _, model_type = extract_inner_model(annotation)
                if isinstance(model_type, type) and issubclass(model_type, BaseModel):
                    result["model_sub_class"].append(field_name)
                else:
                    result["model_class"].append(field_name)
            except ValueError:
                result["model_class"].append(field_name)

    return result
