from flask import Blueprint, request, jsonify
from api.v1.views.utils import create_student_token, student_required, create_teacher_token, create_admin_token
from models import storage
from models.users import User

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


@app_views.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Not a JSON"}), 404

    if 'id' not in data or 'password' not in data:
        return jsonify({"error": "Missing id or password"}), 400

    user = storage.get_first(User, id=data['id'])
    if user and user.check_password(data['password']):
        if user.role == 'Student':
            access_token = create_student_token(user.id)
        elif user.role == 'Teacher':
            access_token = create_teacher_token(user.id)
        elif user.role == 'Admin':
            access_token = create_admin_token(user.id)
        else:
            return jsonify({"error": "Invalid role"}), 401
        return jsonify(access_token=access_token, role=user.role), 200

    return jsonify({"error": "Invalid credentials"}), 401
