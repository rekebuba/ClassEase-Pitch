#!/usr/bin/python3
from models import storage
from api.v1.views import app_views
from api.v1.views import auth
from models.users import User
from flask import Flask, jsonify, request, abort, make_response
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# create an instance of the Flask class
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET")

# Initialize the JWT manager
jwt = JWTManager(app)


app.register_blueprint(app_views)
app.register_blueprint(auth)


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    app.run(host=host, port=port, debug=True) 
