#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/api/v1/admin')
teach = Blueprint('teach', __name__, url_prefix='/api/v1/teacher')
stud = Blueprint('stud', __name__, url_prefix='/api/v1/student')
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


from api.v1.views.admin import *
from api.v1.views.students import *
from api.v1.views.teachers import *
