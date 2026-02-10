import logging
import random
import re
from dataclasses import dataclass
from datetime import date, datetime
from typing import (
    Annotated,
    Any,
    List,
    Tuple,
    Type,
    TypedDict,
    Union,
    get_args,
    get_origin,
)

import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from pyethiodate import EthDate
from sqlalchemy import select
from sqlalchemy.orm import Session

from project.core import security
from project.core.config import settings
from project.models.grade import Grade
from project.models.user import User
from project.models.year import Year
from project.utils.enum import RoleEnum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EmailData:
    html_content: str
    subject: str


def verify_password_reset_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[security.ALGORITHM],
        )
        return str(decoded_token["sub"])
    except InvalidTokenError:
        return None


def generate_subject_code(subject: str) -> str:
    # Split the subject name into words
    words = subject.split()

    """Determine the length of the prefix for each word
    (2 letters if multiple words, 3 otherwise)"""
    prefix_length = 3

    """Generate the base code by taking the first 'prefix_length'
      characters of each word and converting them to uppercase"""
    code = "".join(
        [
            word[:prefix_length].upper()
            for word in words
            if word.isalpha() and word != "and"
        ]
    )
    return code


def sort_grade_key(grade: Grade) -> tuple[int, int | str]:
    grade_value = grade.grade.value  # Get the actual enum value
    if grade_value.isdigit():
        return (1, int(grade_value))  # Numbers: type=1, numeric value
    else:
        return (0, grade_value)  # Strings: type=0, string value


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


def current_EC_year(date: date | datetime) -> Any:
    return EthDate.to_ethiopian(date.year, date.month, date.day)["year"]


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


def generate_id(
    *,
    session: Session,
    role: RoleEnum,
    year: Year,
    min_val: int = 1000,
    max_val: int = 9999,
    max_attempts: int = 100,
    base_sample_size: int = 5,
) -> str:
    """
    Generates a custom ID based on the role (Admin, Student, Teacher).

    Args:
        role: RoleEnum representing the user role (Admin, Student, Teacher)
        year: Academic year
        min_val: Minimum value of ID range (inclusive)
        max_val: Maximum value of ID range (inclusive)
        max_attempts: Maximum number of retries
        base_sample_size: Number of random samples to generate per attempt

    The ID format is: <section>/<random_number>/<year_suffix>
    - Section: 'MAS' for Student, 'MAT' for Teacher, 'MAA' for Admin
    - Random number: A 4-digit number between 1000 and 9999
    - Year suffix: Last 2 digits of the current Ethiopian year

    Returns:
        A unique username string.

    Raises:
        ValueError: If a unique ID could not be generated in time.
    """
    section: str = ""
    year_start = current_EC_year(year.start_date)
    year_end = current_EC_year(year.end_date)
    academic_year = int(year_start) if year_start == year_end else int(year_end)

    # Assign prefix based on role
    if role == RoleEnum.STUDENT:
        section = "MAS"
    elif role == RoleEnum.TEACHER:
        section = "MAT"
    elif role == RoleEnum.ADMIN:
        section = "MAA"
    else:
        raise ValueError(f"Invalid role: {role}")

    sample_size = base_sample_size
    attempts = 0

    while attempts < max_attempts:
        random_ids = {random.randint(min_val, max_val) for _ in range(sample_size)}

        existing_ids = session.scalars(
            select(User.username).where(
                User.username.in_(
                    [f"{section}/{rid}/{academic_year % 100}" for rid in random_ids]
                )
            )
        ).all()

        existing_rids = {
            int(id.split("/")[1])
            for id in existing_ids
            if id and "/" in id and len(id.split("/")) == 3
        }

        available_ids = random_ids - existing_rids
        if available_ids:
            chosen_id = random.choice(list(available_ids))
            return f"{section}/{chosen_id}/{academic_year % 100}"

        sample_size += base_sample_size
        attempts += 1

    raise ValueError(
        "Failed to generate a unique username number after multiple attempts."
    )
