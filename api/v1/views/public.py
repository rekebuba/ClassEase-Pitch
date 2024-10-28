from flask import Blueprint, request, jsonify
from api.v1.views.utils import create_student_token, student_required, create_teacher_token, create_admin_token
from models import storage
from models.users import User
from urllib.parse import urlparse, parse_qs

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


@app_views.route('/login', methods=['GET'])
def login():
    url = request.url
    parsed_url = urlparse(url)
    data = parse_qs(parsed_url.query)

    required_fields = {'id', 'password'}
    for field in required_fields:
        if field not in data:
            return jsonify({"error": "Missing id or password"}), 400

    if 'id' not in data or 'password' not in data:
        return jsonify({"error": "Missing id or password"}), 400

    print(data)
    user = storage.get_first(User, id=data['id'][0])
    if user and user.check_password(data['password'][0]):
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
