from flask import request, jsonify, abort
from models import storage
from models.users import User
from api.v1.views import app_views
from flask_jwt_extended import jwt_required
import jwt
import os

@app_views.route('/home', methods=['GET'])
@jwt_required()
def protected():
    token = request.headers['Authorization'].split(" ")[1]  # Bearer <token>
    data = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
    user_data = storage.get(User, data['sub'])
    return jsonify(user_data), 200
