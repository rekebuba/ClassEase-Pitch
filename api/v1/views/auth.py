#!/usr/bin/python3

from flask import request, jsonify, abort
from models import storage
from models.users import User
from api.v1.views import app_views
from api.v1.views import auth
from flask_jwt_extended import create_access_token, jwt_required
import datetime
import jwt
import os

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        abort(400, description="Not a JSON")

    user = User(name=data['name'], email=data['email'])
    user.hash_password(data['password'])
    
    storage.add(user)
    return jsonify({"message": "User registered successfully!"}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = storage._DBStorage__session.query(User).filter_by(email=data['email']).first()

    if user and user.check_password(data['password']):
        expires = datetime.timedelta(hours=1)
        access_token = create_access_token(identity=user.id, expires_delta=expires)
        return jsonify(access_token=access_token), 200

    return jsonify({"error": "Invalid credentials"}), 401


