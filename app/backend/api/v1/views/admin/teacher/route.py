from typing import Tuple
from urllib.parse import parse_qs, urlparse

from flask import Response, jsonify, request, url_for
from api.v1.utils.typing import UserT
from api.v1.views.admin import admins as admin
from api.v1.views.utils import admin_required
from models.teacher import Teacher
from models.user import User
from models import storage


@admin.route("/teachers", methods=["GET"])
@admin_required
def all_teachers(admin_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve and return a list of teachers with pagination and optional search functionality.

    Args:
        admin_data (dict): Data related to the admin making the request.
    """
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    query = (
        storage.session.query(
            Teacher.id,
            Teacher.first_name.label("firstName"),
            Teacher.last_name.label("lastName"),
            Teacher.email,
            Teacher.no_of_mark_list.label("markList"),
            User.image_path,
        )
        .join(User, User.id == Teacher.id)
        .group_by(Teacher.id)
    )

    if not query:
        return jsonify({"message": "No teachers found"}), 404

    teacher_list = [
        {
            key: url_for("static", filename=value, _external=True)
            if key == "image_path" and value is not None
            else value
            for key, value in q._asdict().items()
        }
        for q in query
    ]

    return jsonify(
        {
            "teachers": teacher_list,
        }
    ), 200
