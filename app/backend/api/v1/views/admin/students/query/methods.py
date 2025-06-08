from typing import Any, Dict

from api.v1.utils.typing import (
    QueryStudentTableId,
    QueryStudentsData,
)


def extract_table_id(item: Dict[str, Any]) -> QueryStudentTableId:
    table_id: QueryStudentTableId = {}
    if not item:
        return table_id

    for k, entry in item.items():
        if isinstance(entry, dict):
            user_table_id = entry.pop("tableId", None)
            for key in entry:
                if isinstance(entry[key], dict):
                    custom_key = "_".join(entry[key].keys())
                    table_id.setdefault(custom_key, user_table_id)
                else:
                    table_id.setdefault(key, user_table_id)

    return table_id


def flatten_keys(item: Dict[str, Any]) -> QueryStudentsData:
    """
    Flatten nested keys in the given item dictionary.
    """
    # Safely build full name from nested fields
    name_parts = item.get("student", {}).pop("studentName", {})
    custom_key = "_".join(name_parts.keys())
    full_name = " ".join(
        name_parts.get(k, "") for k in ("firstName", "fatherName", "grandFatherName")
    ).strip()
    item["student"][custom_key] = full_name

    # Flatten all specified keys into the result
    result = {}

    for key, value in item.items():
        if isinstance(value, dict):
            result.update(value)  # Flatten one level of nesting
        else:
            result[key] = value

    # Remove unwanted key
    result.pop("tableId", None)

    return result
