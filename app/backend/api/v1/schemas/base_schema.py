from datetime import datetime
import re
from marshmallow import Schema, ValidationError, post_dump, post_load, validates
from pyethiodate import EthDate


def to_snake(data):
    if isinstance(data, dict):
        return {to_snake_case_key(k): to_snake(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [to_snake(item) for item in data]
    else:
        return data


def to_camel(data):
    if isinstance(data, dict):
        return {to_camel_case_key(k): to_camel(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [to_camel(item) for item in data]
    else:
        return data


def to_snake_case_key(s):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()


def to_camel_case_key(s):
    parts = s.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])


class BaseSchema(Schema):
    """Base schema with global Case conversion."""

    @post_dump
    def convert_to_camel_case(self, data, **kwargs):
        """Convert keys to camelCase when serializing (dumping)."""
        return to_camel(data)

    @post_load
    def convert_to_snake_case(self, data, **kwargs):
        """Convert keys to snake_case when deserializing (loading)."""
        return to_snake(data)

    def validate_phone(self, value):
        pattern = r'^\+?[0-9]{1,3}[-.\s]?\(?[0-9]{1,4}\)?[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,9}$'

        # Check if the phone number matches the pattern
        if not re.match(pattern, value):
            raise ValidationError("Invalid phone number format.")

    def current_EC_year(self) -> str:
        return str(EthDate.date_to_ethiopian(datetime.now()).year)

    def current_GC_year(self, ethiopian_year: int) -> str:
        return f'{ethiopian_year + 7}/{ethiopian_year + 8}'
