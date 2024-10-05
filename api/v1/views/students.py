from flask import request, jsonify, abort
from models import storage
from models.users import User
from models.grades import Grade
from models.student import Student
from models.section import Section
from api.v1.views import app_views
from flask_jwt_extended import jwt_required
import jwt


@app_views.route('/student/registration', methods=['POST'])
def register_new_student():
    data = request.get_json()

    if not data:
        abort(400, description="Not a JSON")


    grade = storage._DBStorage__session.query(Grade).filter_by(name=data['grade']).first()
    if not grade:
        grade = Grade(name=data['grade'])
        storage.add(grade)

    section = storage._DBStorage__session.query(Section).filter_by(grade_id=grade.id).first()
    if not section:
        section = Section(name='A', grade_id=grade.id, grade=grade)
        storage.add(section)

    new_student = Student(name=data['name'], grade_id=grade.id, section_id=section.id)
    storage.add(new_student)

    return  jsonify({"message": "Student registered successfully!"}), 201
