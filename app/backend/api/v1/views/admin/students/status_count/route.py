from typing import Tuple

from flask import Response, jsonify
from sqlalchemy import case, func
from api.v1.utils.typing import UserT
from api.v1.views.admin import admins as admin
from api.v1.views.admin.students.status_count.schema import (
    StudentStatusSchema,
)
from api.v1.views.utils import admin_required

from models.student import Student
from models.user import User
from models import storage


@admin.route("/students/status-count", methods=["GET"])
@admin_required
def student_status_count(admin_data: UserT) -> Tuple[Response, int]:
    """
    Retrieve and return the count of students based on their status.

    Returns:
        Response: A JSON response containing the count of students based on their status.
                  If no students are found, returns a 404 error with an appropriate message.
    """
    query = (
        storage.session.query(
            func.count(case((Student.is_active == True, 1), else_=None)).label(
                "active"
            ),
            func.count(case((Student.is_active == False, 1), else_=None)).label(
                "inactive"
            ),
            func.count(case((Student.is_active == None, 1), else_=None)).label(
                "suspended"
            ),
        )
        .join(User.students)
        .outerjoin(Student.year_records)
    )

    # Process results
    result = query.one()
    data_to_serialize = {
        "active": result.active,
        "inactive": result.inactive,
        "suspended": result.suspended,
    }
    # Return the serialized data
    schema = StudentStatusSchema()
    send_result = schema.load(data_to_serialize)

    return jsonify(**send_result), 200
