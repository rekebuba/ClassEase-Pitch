import re
from marshmallow import Schema, post_dump, post_load


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
