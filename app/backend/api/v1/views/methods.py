import json
import os
from models import storage
from typing import Any, Callable, Dict, List, Tuple, Type, Union
from flask import current_app, request, jsonify
from math import ceil
from marshmallow import Schema
from sqlalchemy import and_, case, func
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from api.v1.schemas.schemas import AdminSchema, StudentSchema, TeacherSchema
from models.admin import Admin
from models.base_model import CustomTypes
from models.student import Student
from models.teacher import Teacher
from models.user import User
from models.semester import Semester
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm import Query


def create_user(data: Dict[str, Any]) -> User:
    # Save the profile picture if exists
    filepath = None
    if "image_path" in data and isinstance(data["image_path"], FileStorage):
        filepath = save_profile(data["image_path"])
        data["image_path"] = filepath

    # Create the user
    new_user = User(**data)

    storage.add(new_user)
    storage.session.flush()  # Flush to get the new_user.id

    return new_user


def create_role_based_user(
    role_enum: CustomTypes.RoleEnum, data: Dict[str, Any]
) -> User | None:
    role_mapping: Dict[
        CustomTypes.RoleEnum,
        Tuple[Type[Schema], Union[Type[Admin], Type[Student], Type[Teacher]]],
    ] = {
        CustomTypes.RoleEnum.ADMIN: (AdminSchema, Admin),
        CustomTypes.RoleEnum.STUDENT: (StudentSchema, Student),
        CustomTypes.RoleEnum.TEACHER: (TeacherSchema, Teacher),
    }

    if role_enum in role_mapping:
        schema_class, model_class = role_mapping[role_enum]
        schema = schema_class()
        validated_data = schema.load(data)

        new_user = create_user(validated_data.pop("user"))

        new_instance = model_class(user_id=new_user.id, **validated_data)
        storage.add(new_instance)
        storage.save()
        return new_user

    return None


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

    :param query: SQLAlchemy query object to paginate
    :param page: Current page number
    :param limit: Number of records per page
    :param filters: List of filter conditions
    :param custom_filters: List of custom filter conditions
    :param sort: List of sort conditions
    :param join: Function to join filters (default: and_)
    :return: Dictionary with paginated data and meta information
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


def validate_request(required_fields, file_fields=[]):
    """Checks for required form and file fields in the request."""
    missing_fields = [field for field in required_fields if not request.form.get(field)]
    missing_files = [field for field in file_fields if not request.files.get(field)]

    if missing_fields or missing_files:
        return jsonify(
            {"message": f"Missing fields: {', '.join(missing_fields + missing_files)}"}
        ), 400

    return None  # No errors


def preprocess_query_params(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert parse_qs output and handle comma-separated values."""
    processed = {}
    for key, value in data.items():
        # parse_qs always gives lists, so we take first element
        str_value = value[0] if value else ""

        # Check if the value contains commas (but not for certain keys)
        if "," in str_value and key not in ["exclude_comma_keys"]:
            processed[key] = [item.strip() for item in str_value.split(",")]
        if key in ["sort", "filters"]:
            # take first item and parse JSON
            processed[key] = json.loads(value[0])
        else:
            # Single value (keep as string, or convert later in schema)
            processed[key] = str_value
    return processed


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
