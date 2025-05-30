from dataclasses import asdict
from typing import Any, Dict, List

from marshmallow import ValidationError
from sqlalchemy import ColumnElement

from api.v1.schemas.config_schema import OPERATOR_MAPPING
from api.v1.utils.typing import (
    BuiltValidFilterDict,
    BuiltValidSortDict,
    PostFilterDict,
    PostLoadParam,
    PostSortDict,
    QueryStudentTableId,
    QueryStudentsData,
)


def extract_table_id(item: Dict[str, Any]) -> QueryStudentTableId:
    table_id: QueryStudentTableId = {}
    if not item:
        return table_id

    for model in item.keys():
        entries = item[model]
        if not isinstance(entries, list):
            entries = [entries]

        for entry in entries:
            if isinstance(entry, dict):
                user_table_id = entry.pop("tableId", None)
                for key in entry:
                    if isinstance(entry[key], dict):
                        table_id[key] = [(k, user_table_id) for k in entry[key]]
                    else:
                        table_id.setdefault(key, user_table_id)

    return table_id


def flatten_keys(item: Dict[str, Any]) -> QueryStudentsData:
    """
    Flatten nested keys in the given item dictionary.
    """
    # Safely build full name from nested fields
    name_parts = item.get("student", {}).pop("studentName", {})
    full_name = " ".join(
        name_parts.get(k, "") for k in ("firstName", "fatherName", "grandFatherName")
    ).strip()
    item["student"]["studentName"] = full_name

    # Flatten all specified keys into the result
    result: Dict[str, Any] = {}

    for key, value in item.items():
        if isinstance(value, dict):
            result.update(value)  # Flatten one level of nesting
        else:
            result[key] = value

    # Remove unwanted key
    result.pop("tableId", None)

    return result


def build_valid_sort(
    valid_sort_data: List[PostSortDict], custom_types: Dict[str, ColumnElement[Any]]
) -> BuiltValidSortDict:
    valid_sorts: BuiltValidSortDict = {
        "valid_sorts": [],
        "custom_sorts": [],
    }

    for sorts in valid_sort_data:
        if not sorts["valid_sorts"] and sorts["custom_sorts"]:
            column_name = sorts["custom_sorts"]["column_name"]
            is_desc = sorts["custom_sorts"].get("desc", False)

            expr = custom_types.get(column_name)
            if expr is None:
                raise ValidationError(f"Invalid custom sort: {column_name}")

            valid_sorts["custom_sorts"].append(expr.desc() if is_desc else expr)
        else:
            # If no custom sort is provided, use a default sort to avoid empty queries
            valid_sorts["valid_sorts"].extend(sorts["valid_sorts"])

    return valid_sorts


def build_valid_filter(
    valid_filter_data: List[PostFilterDict], custom_types: Dict[str, ColumnElement[Any]]
) -> BuiltValidFilterDict:
    """Builds valid filters from the provided filter data."""
    valid_filters: BuiltValidFilterDict = {
        "valid_filters": [],
        "custom_filters": [],
    }

    for filters in valid_filter_data:
        if not filters["valid_filters"] and filters["custom_filters"]:
            column_name = filters["custom_filters"]["column_name"]
            operator = filters["custom_filters"]["operator"]
            value = filters["custom_filters"]["value"]

            expr = custom_types.get(column_name)
            if expr is None:
                raise ValidationError(f"Invalid custom filter: {column_name}")

            op_func = OPERATOR_MAPPING.get(operator)
            if op_func is None:
                raise ValidationError(f"Unsupported operator: {operator}")

            try:
                condition = op_func(expr, value)
            except Exception as e:
                raise ValidationError(f"Invalid value for operator '{operator}': {e}")
            valid_filters["custom_filters"].append(condition)
        else:
            # If no filters are provided, use a default filter to avoid empty queries
            valid_filters["valid_filters"].extend(filters["valid_filters"])

    return valid_filters
