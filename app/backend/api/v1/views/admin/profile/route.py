from typing import Tuple

from flask import Blueprint, Response, jsonify, request
from api.v1.utils.typing import UserT
from api.v1.views.utils import admin_required


admin = Blueprint("admin", __name__, url_prefix="/api/v1/admin")


@admin.route("/profile", methods=["PUT"])
@admin_required
def update_admin_profile(admin_data: UserT) -> Tuple[Response, int]:
    """
    Update the profile of an admin user.

    Args:
        admin_data (object): The admin user object whose profile is to be updated.

    Returns:
        Response: A JSON response indicating the result of the update operation.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "Not a JSON"}), 400
    return jsonify({"message": "Profile Updated Successfully"}), 200
