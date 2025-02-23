import os
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


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_profile(data):
    # Validate file type and save it
    try:
        profile = data['profilePicture']

        if profile and allowed_file(profile.filename):
            filename = secure_filename(profile.filename)
            base_dir = os.path.abspath(os.path.dirname("static"))
            static_dir = os.path.join(base_dir, 'api/v1/static')
            filepath = os.path.join(
                static_dir, current_app.config['UPLOAD_FOLDER'], filename)
            profile.save(filepath)

            # Return the file path
            return os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        else:
            return None
    except Exception as e:
        return None


def validate_request(required_fields, file_fields=[]):
    """Checks for required form and file fields in the request."""
    missing_fields = [
        field for field in required_fields if not request.form.get(field)]
    missing_files = [
        field for field in file_fields if not request.files.get(field)]

    if missing_fields or missing_files:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields + missing_files)}"}), 400

    return None  # No errors
