import json
import uuid
import random
from faker import Faker
from models import storage
from models.admin import Admin
from models.teacher import Teacher
from models.student import Student
from datetime import datetime


def generate_students(num=1):
    f = Faker()

    rows = [{
        'name': f.first_name(),
        'father_name': f.last_name_male(),
        'grand_father_name': f.last_name_male(),
        'grade': 1,
        'date_of_birth': f.date_of_birth(minimum_age=3, maximum_age=20).strftime('%Y-%m-%dT%H:%M:%S.%f'),
        "father_phone": f.phone_number(),
        "mother_phone": f.phone_number(),
        "start_year": f"2024/25"
    }
        for _ in range(num)]
    return rows


def generate_teachers(num=1):
    f = Faker()
    rows = [{
        'first_name': f.first_name(),
        'last_name': f.last_name_male(),
        'age': random.randint(20, 60),
        'gender': random.choice(["male", "female"]),
        "email": f.email(),
        "phone": f.phone_number(),
        "address": f.address(),
        "experience": random.randint(0, 5),
        "qualification": random.choice(["Certified Teacher"]),
        "subject_taught": random.choice(["Math", "English", "Physics", "Chemistry", "Biology", "History", "Geography", "Art", "Music", "Physical Education", "Science"]),
    }
        for _ in range(num)]
    return rows


def generate_admin(num=1):
    f = Faker()
    rows = [{
        'name': f.first_name(),
        'email': f.email(),
    }
        for _ in range(num)]
    return rows


def generate_mark_list_data(num=1):
    f = Faker()
    return {
        "grade": 1,
        "sections": ["A", "B"],
        "subjects": [
            "Math", "English", "Physics", "Chemistry", "Biology", "History", "Geography", "Art", "Music", "Physical Education", "Science"
        ],
        "assessment_type": [
            {"type": "midterm", "percentage": random.randint(10, 50)},
            {"type": "final", "percentage": random.randint(50, 90)},
            {"type": "quiz", "percentage": random.randint(5, 20)}
        ],
        "semester": random.randint(1, 2),
        "year": "2024/25"
    }


def register_admin(client):
    """Register an admin for testing."""

    # Register an admin before login
    admins = generate_admin(1)
    try:
        for admin in admins:
            response = client.post('/api/v1/admin/registration',
                                   data=json.dumps(admin), content_type='application/json')
            if response.status_code != 201:
                raise Exception
    except Exception as e:
        return response

    return response


def register_teacher(client):
    """Register an teacher for testing."""

    teachers = generate_teachers(1)
    try:
        for teacher in teachers:
            response = client.post('/api/v1/admin/teachers/registration',
                                   data=json.dumps(teacher), content_type='application/json')
            if response.status_code != 201:
                raise Exception
    except Exception as e:
        return response

    return response


def register_student(client):
    """Register a student for testing."""

    students = generate_students(1)
    response = None
    try:
        for student in students:
            response = client.post('/api/v1/student/registration',
                                   data=json.dumps(student), content_type='application/json')
            if response.status_code != 201:
                raise Exception
    except Exception as e:
        return response

    return response


def get_admin_access_token(client):
    """Get the access token for the admin."""
    register_admin(client)

    id = storage.get_random(Admin).id

    # Test that a valid login returns a token
    response = client.get(
        f'/api/v1/login?id={id}&password={id}', content_type='application/json')

    json_data = response.get_json()
    return json_data['access_token']


def get_teacher_access_token(client):
    """Get the access token for the teacher."""
    register_teacher(client)
    id = storage.get_random(Teacher).id

    # Test that a valid login returns a token
    response = client.get(
        f'/api/v1/login?id={id}&password={id}', content_type='application/json')

    json_data = response.get_json()
    return json_data['access_token']


def get_student_access_token(client):
    """Get the access token for the student."""
    register_student(client)
    id = storage.get_random(Student).id

    # Test that a valid login returns a token
    response = client.get(
        f'/api/v1/login?id={id}&password={id}', content_type='application/json')

    json_data = response.get_json()
    return json_data['access_token']


def create_mark_list(client):
    """Create a mark list for testing."""
    try:
        token = get_admin_access_token(client)

        if not token:
            raise Exception

        for _ in range(5):
            response = register_student(client)
            if response.status_code != 201:
                raise Exception

        response = client.put('/api/v1/admin/students/mark_list',
                              data=json.dumps(generate_mark_list_data(1)),
                              headers={
                                  'Authorization': f'Bearer {token}'},
                              content_type='application/json')

        if response.status_code != 201:
            raise Exception
    except Exception as e:
        return None
    return token


def admin_course_assign_to_teacher(client):
    """Test that an admin can access teacher course data."""
    # Test that a valid login returns a token
    token = create_mark_list(client)
    if not token:
        client.fail("Mark list creation failed. Test failed")

    teacher_token = get_teacher_access_token(client)

    if not teacher_token:
        client.fail(
            "Token not generated. Test failed. Check the login endpoint.")

    response = client.get('/api/v1/admin/teachers',
                                headers={
                                    'Authorization': f'Bearer {token}'},
                                content_type='application/json')

    if response.status_code != 200:
        client.fail("Teacher data not found. Test failed.")

    teachers_data = response.json

    random_entry = random.choice(teachers_data['teachers'])
    teacher_id = random_entry.get('id')

    response = client.put(f'/api/v1/admin/assign-teacher',
                                data=json.dumps(
                                    {
                                        "teacher_id": teacher_id,
                                        "grade": 1,
                                        "section": ["A", "B"],
                                        "subjects_taught": teachers_data['teachers'][0]['subjects'],
                                        "mark_list_year": "2024/25"
                                    }
                                ),
                                headers={
                                    'Authorization': f'Bearer {token}'},
                                content_type='application/json')

    return teacher_token
