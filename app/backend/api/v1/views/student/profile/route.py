from typing import Tuple
from flask import Response, jsonify, request
from api.v1.utils.typing import UserT
from api.v1.views.utils import student_required
from api.v1.views.student import stud
from models.user import User
from models import storage


@stud.route("/profile", methods=["PUT"])
@student_required
def update_student_profile(student_data: UserT) -> Tuple[Response, int]:
    """
    Update the profile of a student with the provided data.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "Not a JSON"}), 400

    required_data = {
        "date_of_birth",
        "father_phone",
        "mother_phone",
    }

    for field in required_data:
        if field not in data:
            return jsonify({"message": f"Missing {field}"}), 400

    student_data.date_of_birth = data["date_of_birth"]
    student_data.father_phone = data["father_phone"]
    student_data.mother_phone = data["mother_phone"]

    print(student_data)
    if "new_password" in data:
        if "current_password" not in data:
            return jsonify({"message": "Missing old password"}), 400
        user = storage.get_first(User, id=student_data.student_id)
        if not user:
            return jsonify({"message": "User not found"}), 404
        if not user.check_password(data["current_password"]):
            return jsonify({"message": "Incorrect password"}), 400

        user.hash_password(data["new_password"])
    storage.save()

    return jsonify({"message": "Profile Updated Successfully"}), 200
