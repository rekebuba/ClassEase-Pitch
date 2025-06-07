from datetime import date, datetime, timedelta
import re
from sqlalchemy import Function, and_, func, or_, true
from sqlalchemy.sql.elements import ColumnElement
from api.v1.utils.typing import RangeDict
from models.base_model import Base, BaseModel
from typing import Any, Callable, Dict, Type, Union, cast


def is_date(val: Any) -> bool:
    """
    Check if the value is a date or datetime object.
    """
    if isinstance(val, list):
        return all(isinstance(v, (date, datetime)) for v in val)
    return isinstance(val, (date, datetime))


def normalize_date_col(col: ColumnElement[Any], val: Any) -> ColumnElement[Any]:
    return cast(ColumnElement[Any], func.date(col)) if is_date(val) else col


OPERATOR_MAPPING: Dict[
    str,
    Callable[
        [Union[Function[Any], ColumnElement[Any]], Union[Any, RangeDict]],
        ColumnElement[Any],
    ],
] = {
    # Equals operators (string only)
    "eq": lambda col, val: (
        normalize_date_col(col, val) == val if isinstance(val, str) else true()
    ),
    "ne": lambda col, val: (
        normalize_date_col(col, val) != val if isinstance(val, str) else true()
    ),
    "lt": lambda col, val: (
        normalize_date_col(col, val) < val if isinstance(val, str) else true()
    ),
    "lte": lambda col, val: (
        normalize_date_col(col, val) <= val if isinstance(val, str) else true()
    ),
    "gt": lambda col, val: (
        normalize_date_col(col, val) > val if isinstance(val, str) else true()
    ),
    "gte": lambda col, val: (
        normalize_date_col(col, val) >= val if isinstance(val, str) else true()
    ),
    "iLike": lambda col, val: col.ilike(f"%{val}%"),
    "like": lambda col, val: col.like(f"%{val}%"),
    "notLike": lambda col, val: ~col.like(f"%{val}%"),
    "startsWith": lambda col, val: col.like(f"{val}%"),
    "endWith": lambda col, val: col.like(f"%{val}"),
    # IN operator (list of values)
    "in": lambda col, val: (
        normalize_date_col(col, val[0]).in_(val)
        if isinstance(val, list) and val
        else normalize_date_col(col, val).in_([val])
        if isinstance(val, str)
        else true()
    ),
    "notIn": lambda col, val: (
        ~normalize_date_col(col, val[0]).in_(val)
        if isinstance(val, list) and val
        else ~normalize_date_col(col, val).in_([val])
        if isinstance(val, str)
        else true()
    ),
    "isEmpty": lambda col, _: or_(true(), col.is_(None), col == ""),
    "isNotEmpty": lambda col, _: and_(true(), col.isnot(None), col != ""),
    "isBetween": lambda col, range: (
        normalize_date_col(col, range.get("min") or range.get("max")).between(
            range.get("min"), range.get("max")
        )
        if isinstance(range, dict)
        and range.get("min") is not None
        and range.get("max") is not None
        else normalize_date_col(col, range.get("min")) >= range.get("min")
        if isinstance(range, dict) and range.get("min") is not None
        else normalize_date_col(col, range.get("max")) <= range.get("max")
        if isinstance(range, dict) and range.get("max") is not None
        else true()
    ),
    "isRelativeToToday": lambda col, days: (
        func.date(col) >= (datetime.utcnow().date() + timedelta(days=days))
        if isinstance(days, int)
        else true()
    ),
}

OPERATOR_CONFIG = {
    "text": ["iLike", "notLike", "startsWith", "endWith", "eq"],
    "number": ["eq", "ne", "lt", "lte", "gt", "gte"],
    "select": ["eq", "ne", "isEmpty", "isNotEmpty"],
    "multiSelect": ["in", "notIn", "isEmpty", "isNotEmpty"],
    "date": [
        "eq",
        "ne",
        "lt",
        "lte",
        "gt",
        "gte",
        "isBetween",
        "isRelativeToToday",
        "isEmpty",
        "isNotEmpty",
    ],
    "dateRange": [
        "eq",
        "ne",
        "lt",
        "lte",
        "gt",
        "gte",
        "isBetween",
        "isRelativeToToday",
        "isEmpty",
        "isNotEmpty",
    ],
    "boolean": ["eq", "ne"],
}

VALUE_TYPE_RULES = {
    "text": str,
    "number": (int, float),
    "multiSelect": (str, list),
    "boolean": bool,
    "dateRange": (datetime, date),
}

ALISA_NAME: Dict[str, Dict[str, Union[str, int, None]]] = {
    "section_semester_one": {"key": "section", "default": 1},
    "section_semester_two": {"key": "section", "default": -1},
    "average_semester_one": {"key": "average", "default": 1},
    "average_semester_two": {"key": "average", "default": -1},
    "rank_semester_one": {"key": "rank", "default": 1},
    "rank_semester_two": {"key": "rank", "default": -1},
    "semester_one": {"key": "name", "default": None},
    "semester_two": {"key": "name", "default": None},
}


def to_snake(data: Any) -> Any:
    """Recursively convert all dictionary keys to snake_case."""
    if isinstance(data, dict):
        return {to_snake_case_key(k): to_snake(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [to_snake(item) for item in data]
    else:
        return data


def to_camel(data: Any) -> Any:
    """Recursively convert all dictionary keys to camelCase."""
    if isinstance(data, dict):
        return {to_camel_case_key(str(k)): to_camel(v) for k, v in data.items()}
    if isinstance(data, list):
        return [to_camel(item) for item in data]
    return data


def to_snake_case_key(s: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()


def to_camel_case_key(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


# Get all model classes dynamically
def get_all_model_classes() -> Dict[str, Type[Base]]:
    # Returns dict of {__tablename__: model_class}
    return {
        cls.__tablename__: cls
        for cls in BaseModel.registry._class_registry.values()
        if isinstance(cls, type)
        and hasattr(cls, "__tablename__")
        and cls is not BaseModel
    }
