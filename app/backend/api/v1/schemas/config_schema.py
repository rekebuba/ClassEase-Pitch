from datetime import date, datetime, timedelta
import re
from sqlalchemy import Function, and_, false, func, or_, true
from sqlalchemy.sql.elements import ColumnElement
from api.v1.utils.typing import RangeDict
from models.base_model import Base, BaseModel
from typing import Any, Callable, Dict, List, Type, Union, cast


def is_date(val: Any) -> bool:
    """
    Check if the value is a date or datetime object.
    """
    if isinstance(val, list):
        return all(isinstance(v, (date, datetime)) for v in val)
    return isinstance(val, (date, datetime))


def normalize_date_col(col: ColumnElement[Any], val: Any) -> ColumnElement[Any]:
    return cast(ColumnElement[Any], func.date(col)) if is_date(val) else col


def notIn(
    col: Union[Function[Any], ColumnElement[Any]], val: List[Any]
) -> ColumnElement[Any]:
    non_null_vals = [v for v in val if v is not None]
    null_value = None in val  # keep nulls if None is not in val

    conditions = []

    if non_null_vals:
        conditions.append(~col.in_(non_null_vals))

    if null_value:
        conditions.append(col.isnot(None))
    else:
        conditions.append(col.is_(None))

    if not conditions:
        return true()  # no values passed, return a no-op filter

    return and_(*conditions) if null_value else or_(*conditions)


OPERATOR_MAPPING: Dict[
    str,
    Callable[
        [Union[Function[Any], ColumnElement[Any]], Union[Any, RangeDict]],
        ColumnElement[Any],
    ],
] = {
    # Equals operators (string only)
    "eq": lambda col, val: (normalize_date_col(col, val) == val),
    "ne": lambda col, val: (normalize_date_col(col, val) != val),
    "lt": lambda col, val: (normalize_date_col(col, val) < val),
    "lte": lambda col, val: (normalize_date_col(col, val) <= val),
    "gt": lambda col, val: (normalize_date_col(col, val) > val),
    "gte": lambda col, val: (normalize_date_col(col, val) >= val),
    "iLike": lambda col, val: col.ilike(f"%{val}%"),
    "like": lambda col, val: col.like(f"%{val}%"),
    "notLike": lambda col, val: ~col.like(f"%{val}%"),
    "startsWith": lambda col, val: col.like(f"{val}%"),
    "endWith": lambda col, val: col.like(f"%{val}"),
    # IN operator (list of values)
    "in": lambda col, val: (
        or_(
            normalize_date_col(col, val[0]).in_([v for v in val if v is not None]),
            normalize_date_col(col, val[0]).is_(None) if None in val else false(),
        )
        if isinstance(val, list) and val
        else or_(
            normalize_date_col(col, val).in_([val]),
            normalize_date_col(col, val).is_(None) if val is not None else false(),
        )
        if isinstance(val, str)
        else true()
    ),
    "notIn": lambda col, val: (
        notIn(normalize_date_col(col, val[0]), val)
        if isinstance(val, list) and val
        else notIn(normalize_date_col(col, val), [val])
        if isinstance(val, str)
        else true()
    ),
    "isEmpty": lambda col, _: or_(col.is_(None), col == ""),
    "isNotEmpty": lambda col, _: and_(col.isnot(None), col != ""),
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
    "isNotBetween": lambda col, range: (
        and_(
            normalize_date_col(col, range.get("min") or range.get("max"))
            < range.get("min"),
            normalize_date_col(col, range.get("min") or range.get("max"))
            > range.get("max"),
        )
        if isinstance(range, dict)
        and range.get("min") is not None
        and range.get("max") is not None
        else ~normalize_date_col(col, range.get("min")) > range.get("min")
        if isinstance(range, dict) and range.get("min") is not None
        else ~normalize_date_col(col, range.get("max")) < range.get("max")
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
    "range": ["isBetween", "isNotBetween"],
    "boolean": ["eq", "ne"],
    "date": [
        "eq",
        "ne",
        "lt",
        "lte",
        "gt",
        "gte",
        "isBetween",
        "isNotBetween",
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
        "isNotBetween",
        "isRelativeToToday",
        "isEmpty",
        "isNotEmpty",
    ],
    "operators": [
        "iLike",
        "notLike",
        "startsWith",
        "endWith",
        "eq",
        "ne",
        "in",
        "notIn",
        "isEmpty",
        "isNotEmpty",
        "lt",
        "lte",
        "gt",
        "gte",
        "isBetween",
        "isNotBetween",
        "isRelativeToToday",
    ],
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
