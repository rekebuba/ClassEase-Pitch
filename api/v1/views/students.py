from flask import Blueprint, request, jsonify
from models import storage
from models.users import User
from models.grade import Grade
from models.student import Student
from models.section import Section
from api.v1.views.utils import student_required


stud = Blueprint('stud', __name__, url_prefix='/api/v1/student')


@stud.route('/registration', methods=['POST'])
def register_new_student():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Not a JSON"}), 404

    required_data = [
        'name',
        'father_name',
        'g_father_name',
        'age',
        'grade',
        'start_year'
    ]
    # Check if required fields are present
    for field in required_data:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400

    if 'father_phone' not in data and 'mother_phone' not in data:
        return jsonify({"error": "Need to provide at least one phone number"}), 400

    grade = storage.get_first(Grade, grade=data['grade'])
    if not grade:
        return jsonify({"error": "Grade not found"}), 404

    new_student = User(role='Student')
    new_student.hash_password(new_student.id)

    try:
        # Save User first
        storage.add(new_student)

        # Create the Student object, using the same id
        students = Student(id=new_student.id, **data, grade_id=grade.id)

        # Save the Student object
        storage.add(students)
    except Exception as e:
        storage.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Student registered successfully!"}), 201


@stud.route('/dashboard', methods=['GET'])
@student_required
def student_dashboard(student_data):
    return jsonify(student_data.to_dict()), 200
