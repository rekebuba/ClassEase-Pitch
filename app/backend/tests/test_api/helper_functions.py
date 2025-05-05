#!/usr/bin/python3
"""Module for helper functions for testing the API"""

import json
import os
import random
import uuid
from faker import Faker
import requests
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

    rows = [
        {
            "first_name": f.first_name(),
            "father_name": f.last_name_male(),
            "grand_father_name": f.last_name_male(),
            "date_of_birth": str(
                f.date_of_birth(minimum_age=3, maximum_age=20).strftime("%Y-%m-%d")
            ),
            "father_phone": "+2656255123",
            "mother_phone": "+2656255123",
            "gender": random.choice(["M", "F"]),
            "current_grade": 1,
            "national_id": str(uuid.uuid4()),
            "image_path": get_ai_profile_picture(),  # Store the file path,
        }
        for _ in range(num)
    ]
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
    rows = [
        {
            "first_name": f.first_name(),
            "father_name": f.last_name(),
            "grand_father_name": f.first_name(),
            "date_of_birth": str(
                f.date_of_birth(minimum_age=20, maximum_age=60).strftime("%Y-%m-%d")
            ),
            "email": f.email(),
            "gender": random.choice(["M", "F"]),
            "phone": "095564135",
            "address": f.address(),
            "image_path": get_ai_profile_picture(),  # Store the file path,
            "national_id": str(uuid.uuid4()),
            "year_of_experience": random.randint(0, 5),
            "qualification": random.choice(["Certified Teacher"]),
            "image_path": get_ai_profile_picture(),  # Store the file path,
        }
        for _ in range(num)
    ]
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
    rows = [
        {
            "first_name": f.first_name(),
            "father_name": f.last_name(),
            "grand_father_name": f.first_name(),
            "date_of_birth": str(
                f.date_of_birth(minimum_age=20, maximum_age=60).strftime("%Y-%m-%d")
            ),
            "email": f.email(),
            "gender": random.choice(["M", "F"]),
            "phone": "095564135",
            "address": f.address(),
            "image_path": get_ai_profile_picture(),  # Store the file path,
            "national_id": str(uuid.uuid4()),
        }
        for _ in range(num)
    ]
    return rows


def get_ai_profile_picture():
    url = "https://thispersondoesnotexist.com"
    response = requests.get(url)
    if response.status_code == 200:
        directory = "profiles"
        os.makedirs(directory, exist_ok=True)  # Ensure directory exists

        file_name = f"{directory}/{uuid.uuid4()}.jpg"
        with open(file_name, "wb") as f:
            f.write(response.content)

        return file_name  # Returns the saved file path
    return None


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
            "Math",
            "English",
            "Physics",
            "Chemistry",
            "Biology",
            "History",
            "Geography",
            "Art",
            "Music",
            "Physical Education",
            "Science",
        ],
        "assessment_type": [
            {"type": "midterm", "percentage": random.randint(10, 50)},
            {"type": "final", "percentage": random.randint(50, 90)},
            {"type": "quiz", "percentage": random.randint(5, 20)},
        ],
        "semester": random.randint(1, 2),
        "year": "2024/25",
    }


def register_user(client, role):
    if role == "admin":
        user = generate_admin(1)[0]
    elif role == "teacher":
        user = generate_teachers(1)[0]
    elif role == "student":
        user = generate_students(1)[0]

    local_path = None
    if user.get("image_path"):
        local_path = user.get("image_path")

    data = {**user, "image_path": open(user.pop("image_path"), "rb")}

    response = client.post(
        f"/api/v1/registration/{role}", data=data, content_type="multipart/form-data"
    )

    # remove the file
    if os.path.exists(local_path):
        os.remove(local_path)
    else:
        print("Image Was not provided for deletion")

    return response


def get_admin_api_key(client):
    """Get the access token for the admin."""
    register_user(client, "admin")

    id = storage.get_random(Admin).id

    # Test that a valid login returns a token
    response = client.post(
        "/api/v1/login",
        data=json.dumps({"id": id, "password": id}),
        content_type="application/json",
    )

    json_data = response.get_json()
    return json_data["ApiKey"]


def get_teacher_api_key(client):
    """Get the access token for the teacher."""
    register_user(client, "teacher")
    id = storage.get_random(Teacher).id

    # Test that a valid login returns a token
    response = client.post(
        "/api/v1/login",
        data=json.dumps({"id": id, "password": id}),
        content_type="application/json",
    )

    json_data = response.get_json()
    return json_data["ApiKey"]


def get_student_api_key(client):
    """Get the access token for the student."""
    register_user(client, "student")
    id = storage.get_random(Student).id

    # Test that a valid login returns a token
    response = client.post(
        "/api/v1/login",
        data=json.dumps({"id": id, "password": id}),
        content_type="application/json",
    )

    json_data = response.get_json()
    return json_data["ApiKey"]


def create_mark_list(client):
    """Create a mark list for testing."""
    try:
        token = get_admin_api_key(client)

        if not token:
            raise Exception

        for _ in range(5):
            response = register_user(client, "student")
            if response.status_code != 201:
                raise Exception

        response = client.put(
            "/api/v1/admin/students/mark_list",
            data=json.dumps(generate_mark_list_data()),
            headers={"apiKey": f"Bearer {token}"},
            content_type="application/json",
        )

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

    teacher_token = get_teacher_api_key(client)

    if not teacher_token:
        client.fail("Token not generated. Test failed. Check the login endpoint.")

    response = client.get(
        "/api/v1/admin/teachers",
        headers={"apiKey": f"Bearer {token}"},
        content_type="application/json",
    )

    if response.status_code != 200:
        client.fail("Teacher data not found. Test failed.")

    teachers_data = response.json

    random_entry = random.choice(teachers_data["teachers"])
    teacher_id = random_entry.get("id")

    response = client.put(
        f"/api/v1/admin/assign-teacher",
        data=json.dumps(
            {
                "teacher_id": teacher_id,
                "grade": 1,
                "section": ["A", "B"],
                "subjects_taught": teachers_data["teachers"][0]["subjects"],
                "mark_list_year": "2024/25",
            }
        ),
        headers={"apiKey": f"Bearer {token}"},
        content_type="application/json",
    )

    return teacher_token
