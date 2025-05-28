import os
from typing import Any, Callable, Dict, List
from flask import current_app
from math import ceil
from sqlalchemy import and_, case, func
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from models.semester import Semester
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm import Query


def paginate_query(
    query: Query[Any],
    page: int,
    limit: int,
    filters: List[Any],
    custom_filters: List[Any],
    sort: List[Any],
    join: Callable[..., Any] = and_,
) -> Dict[str, Any]:
    """
    Paginate SQLAlchemy queries.

    query: SQLAlchemy query object to paginate
    page: Current page number
    limit: Number of records per page
    filters: List of filter conditions
    custom_filters: List of custom filter conditions
    sort: List of sort conditions
    join: Function to join filters (default: and_)
    (return): Dictionary with paginated data and meta information
    """

    # Calculate total number of records
    total_items = query.count()

    # Apply filters and sort
    query = query.filter(join(*filters)).having(join(*custom_filters)).order_by(*sort)

    # Calculate offset and apply limit and offset to the query
    offset = (page - 1) * limit
    paginated_query = query.limit(limit).offset(offset)

    # Get the paginated results
    items = paginated_query.all()

    # Calculate total pages
    total_pages = ceil(total_items / limit)

    return {
        "items": items,
        "meta": {
            "total_items": total_items,
            "current_page": page,
            "per_page": limit,
            "total_pages": total_pages,
        },
    }


def save_profile(file: FileStorage) -> str:
    """Save the uploaded file to the server and return the file path."""
    filename = secure_filename(file.filename)
    base_dir = os.path.abspath(os.path.dirname("static"))
    static_dir = os.path.join(base_dir, "api/v1/static")
    upload_folder = os.path.join(static_dir, current_app.config["UPLOAD_FOLDER"])

    # Ensure the upload folder exists
    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    # Return the relative file path
    return os.path.join(current_app.config["UPLOAD_FOLDER"], filename)


def make_case_lookup(
    semester_num: int, column: InstrumentedAttribute[Any], prefix: str
) -> Dict[str, ColumnElement[Any]]:
    """Helper to generate case expressions with dynamic labels."""
    label_I = f"{prefix}I"  # Pre-compute the label
    label_II = f"{prefix}II"

    expr_I = func.max(case((Semester.name == semester_num, column))).label(label_I)
    expr_II = func.max(case((Semester.name == semester_num + 1, column))).label(
        label_II
    )

    return {
        label_I: expr_I,
        label_II: expr_II,
    }


def min_max_semester_lookup(
    semester_num: int, column: InstrumentedAttribute[Any], prefix: str
) -> Dict[str, ColumnElement[Any]]:
    """Helper to generate case expressions with dynamic labels."""
    label_I = f"{prefix}_min"  # Pre-compute the label
    label_II = f"{prefix}_max"

    expr_I = func.min(case((Semester.name == semester_num, column))).label(label_I)
    expr_II = func.max(case((Semester.name == semester_num, column))).label(label_II)

    return {
        label_I: expr_I,
        label_II: expr_II,
    }


def min_max_year_lookup(
    column: InstrumentedAttribute[Any], prefix: str
) -> Dict[str, ColumnElement[Any]]:
    """Helper to generate case expressions with dynamic labels."""
    label_I = f"{prefix}_min"  # Pre-compute the label
    label_II = f"{prefix}_max"

    expr_I = func.min((column)).label(label_I)
    expr_II = func.max((column)).label(label_II)

    return {
        label_I: expr_I,
        label_II: expr_II,
    }


def parse_nested_form(form_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parses a flat form data dictionary into a nested dictionary structure.
    Args:
        form_data (Dict[str, str]): The flat form data dictionary.
    """

    result: Dict[str, Any] = {}
    for key, value in form_data.items():
        parts = key.split(".")
        current = result
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    return result
