import logging
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
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

import emails  # type: ignore
import jwt
from jinja2 import Template
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from pyethiodate import EthDate  # type: ignore

from core import security
from core.config import settings
from models.grade import Grade

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EmailData:
    html_content: str
    subject: str


def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent / "email-templates" / "build" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    return html_content


def send_email(
    *,
    email_to: str,
    subject: str = "",
    html_content: str = "",
) -> None:
    assert settings.emails_enabled, "no provided configuration for email variables"
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    elif settings.SMTP_SSL:
        smtp_options["ssl"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, smtp=smtp_options)
    logger.info(f"send email result: {response}")


def generate_test_email(email_to: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    html_content = render_email_template(
        template_name="test_email.html",
        context={"project_name": settings.PROJECT_NAME, "email": email_to},
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_reset_password_email(email_to: str, email: str, token: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    link = f"{settings.FRONTEND_HOST}/reset-password?token={token}"
    html_content = render_email_template(
        template_name="reset_password.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_new_account_email(
    email_to: str, username: str, password: str
) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    html_content = render_email_template(
        template_name="new_account.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": settings.FRONTEND_HOST,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.now(timezone.utc)
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm=security.ALGORITHM,
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
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
