import json
import os
import re
from flask import current_app, request, jsonify
from math import ceil
from werkzeug.utils import secure_filename


def paginate_query(query, page, limit):
    """
    Paginate SQLAlchemy queries.

    :param query: SQLAlchemy query object to paginate
    :param request: Flask request object to get query parameters (page, limit)
    :param default_limit: Default number of records per page if limit is not provided
    :return: Dictionary with paginated data and meta information
    """

    # Calculate total number of records
    total_items = query.count()

    # Calculate offset and apply limit and offset to the query
    offset = (page - 1) * limit
    paginated_query = query.limit(limit).offset(offset)

    # Get the paginated results
    items = paginated_query.all()

    # Calculate total pages
    total_pages = ceil(total_items / limit)

    # Return the paginated data and meta information
    return {
        "items": items,
        "meta": {
            "total_items": total_items,
            "current_page": page,
            "limit": limit,
            "total_pages": total_pages,
        }
    }


def save_profile(file):
    """Save the uploaded file to the server and return the file path."""
    filename = secure_filename(file.filename)
    base_dir = os.path.abspath(os.path.dirname("static"))
    static_dir = os.path.join(base_dir, 'api/v1/static')
    upload_folder = os.path.join(
        static_dir, current_app.config['UPLOAD_FOLDER'])

    # Ensure the upload folder exists
    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    # Return the relative file path
    return os.path.join(current_app.config['UPLOAD_FOLDER'], filename)


def validate_request(required_fields, file_fields=[]):
    """Checks for required form and file fields in the request."""
    missing_fields = [
        field for field in required_fields if not request.form.get(field)]
    missing_files = [
        field for field in file_fields if not request.files.get(field)]

    if missing_fields or missing_files:
        return jsonify({"message": f"Missing fields: {', '.join(missing_fields + missing_files)}"}), 400

    return None  # No errors


def preprocess_query_params(data):
    """Convert parse_qs output and handle comma-separated values."""
    processed = {}
    for key, value in data.items():
        # parse_qs always gives lists, so we take first element
        str_value = value[0] if value else ''

        # Check if the value contains commas (but not for certain keys)
        if ',' in str_value and key not in ['exclude_comma_keys']:
            processed[key] = [item.strip() for item in str_value.split(',')]
        if key in ['sort', 'filters']:
            # take first item and parse JSON
            processed[key] = json.loads(value[0])
        else:
            # Single value (keep as string, or convert later in schema)
            processed[key] = str_value
    return processed


def paginate_query(query, page, limit):
    """
    Paginate SQLAlchemy queries.

    :param query: SQLAlchemy query object to paginate
    :param request: Flask request object to get query parameters (page, limit)
    :param default_limit: Default number of records per page if limit is not provided
    :return: Dictionary with paginated data and meta information
    """

    # Calculate total number of records
    total_items = query.count()

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
            "limit": limit,
            "total_pages": total_pages,
        }
    }
