from datetime import datetime
from typing import Tuple
import uuid

from flask import Response, jsonify
from api.v1.utils.typing import UserT
from api.v1.views.utils import admin_required
from api.v1.views.admin import admins as admin


@admin.route("/students/views", methods=["GET"])
@admin_required
def student_views(admin_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve and return the views of students.

    Returns:
        Response: A JSON response containing the views of students.
                  If no students are found, returns a 404 error with an appropriate message.
    """
    return jsonify(
        [
            {
                "id": uuid.uuid4(),
                "name": "new View",
                "columns": [""],
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        ]
    ), 200
