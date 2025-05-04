from datetime import date, datetime, timedelta
import re
from sqlalchemy import and_, func, or_

from models.base_model import BaseModel


def is_date(val):
    return isinstance(val, (date, datetime))


def normalize_date_col(col, val):
    return func.date(col) if is_date(val) else col


OPERATOR_MAPPING = {
    "eq": lambda col, val: normalize_date_col(col, val) == val,
    "ne": lambda col, val: normalize_date_col(col, val) != val,
    "lt": lambda col, val: normalize_date_col(col, val) < val,
    "lte": lambda col, val: normalize_date_col(col, val) <= val,
    "gt": lambda col, val: normalize_date_col(col, val) > val,
    "gte": lambda col, val: normalize_date_col(col, val) >= val,
    "iLike": lambda col, val: col.ilike(f"%{val}%"),
    "like": lambda col, val: col.like(f"%{val}%"),
    "notLike": lambda col, val: ~col.like(f"%{val}%"),
    "startsWith": lambda col, val: col.like(f"{val}%"),
    "endWith": lambda col, val: col.like(f"%{val}"),
    "in": lambda col, val: normalize_date_col(col, val[0])
    .in_(val if isinstance(val, list) else [val]) if val else False,
    "notIn": lambda col, val: ~normalize_date_col(col, val[0])
    .in_(val if isinstance(val, list) else [val]) if val else True,
    "isEmpty": lambda col, _: or_(col.is_(None), col == ""),
    "isNotEmpty": lambda col, _: and_(col.isnot(None), col != ""),
    "isBetween": lambda col, range: (
        normalize_date_col(col, range.get("min") or range.get(
            "max")).between(range.get("min"), range.get("max"))
        if range.get("min") is not None and range.get("max") is not None
        else normalize_date_col(col, range.get("min")) >= range.get("min")
        if range.get("min") is not None
        else normalize_date_col(col, range.get("max")) <= range.get("max")
        if range.get("max") is not None
        else None
    ),
    "isRelativeToToday": lambda col, days: (
        func.date(col) >= (datetime.utcnow().date() + timedelta(days=days))
        if isinstance(days, int)
        else None
    )
}

OPERATOR_CONFIG = {
    "text": ["iLike", "notLike", "startsWith", "endWith", "eq"],
    "number": ["eq", "ne", "lt", "lte", "gt", "gte"],
    "select": ["eq", "ne", "isEmpty", "isNotEmpty"],
    "multiSelect": ["in", "notIn", "isEmpty", "isNotEmpty"],
    "date": ["eq", "ne", "lt", "lte", "gt", "gte", "isBetween", "isRelativeToToday", "isEmpty", "isNotEmpty"],
    "dateRange": ["eq", "ne", "lt", "lte", "gt", "gte", "isBetween", "isRelativeToToday", "isEmpty", "isNotEmpty"],
    "boolean": ["eq", "ne"],
}

VALUE_TYPE_RULES = {
    "text": str,
    "number": (int, float),
    "multiSelect": (str, list),
    "boolean": bool,
    "dateRange": (datetime, date),
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
