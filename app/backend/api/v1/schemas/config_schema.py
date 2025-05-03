import re
from sqlalchemy import and_, or_

from models.base_model import BaseModel


OPERATOR_MAPPING = {
    "eq": lambda col, val: col == val,
    "neq": lambda col, val: col != val,
    "lt": lambda col, val: col < val,
    "lte": lambda col, val: col <= val,
    "gt": lambda col, val: col > val,
    "gte": lambda col, val: col >= val,
    "iLike": lambda col, val: col.ilike(f"{val}%"),
    "like": lambda col, val: col.like(f"{val}%"),
    "in": lambda col, val: col.in_(val if isinstance(val, list) else [val]),
    "not_in": lambda col, val: ~col.in_(val if isinstance(val, list) else [val]),
    "isEmpty": lambda col, _: or_(col.is_(None), col == ""),
    "isNotEmpty": lambda col, _: and_(col.isnot(None), col != ""),
    "isBetween": lambda col, min, max: col.between(min, max),
}

OPERATOR_CONFIG = {
    "text": ["iLike", "notLike", "startsWith", "endWith", "eq"],
    "number": ["eq", "ne", "lt", "lte", "gt", "gte"],
    "dateRange": ["eq", "ne", "lt", "lte", "gt", "gte"],
    "multiSelect": ["in", "notIn"],
    "boolean": ["eq", "ne"],
}

VALUE_TYPE_RULES = {
    "text": str,
    "number": (int, float),
    "multiSelect": (str, list),
    "boolean": bool,
    "dateRange": (str, list),
}


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


# Get all model classes dynamically
def get_all_model_classes():
    # Returns dict of {__tablename__: model_class}
    return {
        cls.__tablename__: cls
        for cls in BaseModel.registry._class_registry.values()
        if hasattr(cls, '__tablename__') and cls is not BaseModel
    }
