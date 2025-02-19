#!/usr/bin/python3
""" Module for helper functions for testing the API """

import json
import random
from faker import Faker
from models import storage
from models.admin import Admin
from models.teacher import Teacher
from models.student import Student


def generate_students(num=1):
    """
    Generate a list of dictionaries representing student data.

    Args:
        num (int): The number of student records to generate. Default is 1.

    Returns:
        list: A list of dictionaries, each containing the following keys:
            - 'name' (str): The first name of the student.
            - 'father_name' (str): The last name of the student's father.
            - 'grand_father_name' (str): The last name of the student's grandfather.
            - 'grade' (int): The grade level of the student, default is 1.
            - 'date_of_birth' (str): The date of birth of the student in ISO 8601 format.
            - 'father_phone' (str): The phone number of the student's father.
            - 'mother_phone' (str): The phone number of the student's mother.
            - 'start_year' (str): The start year of the student's academic session, default is "2024/25".
    """
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
    """
    Generate a list of dictionaries, each representing a teacher with randomly generated attributes.

    Args:
        num (int): The number of teacher dictionaries to generate. Default is 1.

    Returns:
        list: A list of dictionaries, each containing the following keys:
            - first_name (str): The first name of the teacher.
            - last_name (str): The last name of the teacher.
            - age (int): The age of the teacher, randomly chosen between 20 and 60.
            - gender (str): The gender of the teacher, randomly chosen between "male" and "female".
            - email (str): The email address of the teacher.
            - phone (str): The phone number of the teacher.
            - address (str): The address of the teacher.
            - experience (int): The years of experience of the teacher, randomly chosen between 0 and 5.
            - qualification (str): The qualification of the teacher, randomly chosen as "Certified Teacher".
            - subject_taught (str): The subject taught by the teacher, randomly chosen from a predefined list of subjects.
    """
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
    """
    Generate a list of dictionaries containing fake admin user data.

    Args:
        num (int): The number of admin user dictionaries to generate. Default is 1.

    Returns:
        list: A list of dictionaries, each containing 'name' and 'email' keys with fake data.
    """
    f = Faker()
    rows = [{
        'name': f.first_name(),
        'email': f.email(),
    }
        for _ in range(num)]
    return rows


def generate_mark_list_data():
    """
    Generates a dictionary containing mock data for a mark list.

    Returns:
        dict: A dictionary containing the following keys:
            - "grade" (int): The grade level.
            - "sections" (list of str): List of section names.
            - "subjects" (list of str): List of subject names.
            - "assessment_type" (list of dict): List of assessment types with their respective percentages.
            - "semester" (int): The semester number (1 or 2).
            - "year" (str): The academic year in "YYYY/YY" format.
    """
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
    """
    Register an admin for testing.

    This function generates a list of admin users and attempts to register 
    each one by sending a POST request to the '/api/v1/admin/registration' 
    endpoint. If the registration is successful, the response status code 
    should be 201. If any registration fails, an exception is raised and 
    the response is returned.

    Args:
        client: The test client used to send HTTP requests.

    Returns:
        response: The response object from the failed registration attempt, 
                  if an exception is raised. Otherwise, returns the response 
                  object from the last successful registration attempt.
    """
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
    """
    Register a teacher for testing.

    This function generates a single teacher using the `generate_teachers` function
    and attempts to register the teacher via a POST request to the '/api/v1/admin/teachers/registration' endpoint.
    If the registration is not successful (i.e., the response status code is not 201), an exception is raised.

    Args:
        client: The test client used to make the POST request.

    Returns:
        response: The response object from the POST request.

    Raises:
        Exception: If the registration is not successful.
    """
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
    response = client.post('/api/v1/login', data=json.dumps({"id": id, "password": id}), content_type='application/json')

    json_data = response.get_json()
    return json_data['access_token']


def get_teacher_access_token(client):
    """Get the access token for the teacher."""
    register_teacher(client)
    id = storage.get_random(Teacher).id

    # Test that a valid login returns a token
    response = client.post('/api/v1/login', data=json.dumps({"id": id, "password": id}), content_type='application/json')

    json_data = response.get_json()
    return json_data['access_token']


def get_student_access_token(client):
    """Get the access token for the student."""
    register_student(client)
    id = storage.get_random(Student).id

    # Test that a valid login returns a token
    response = client.post('/api/v1/login', data=json.dumps({"id": id, "password": id}), content_type='application/json')

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
                              data=json.dumps(generate_mark_list_data()),
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
