import json
import uuid
import random

mark_list_data = {
    "grade": 12,
    "sections": ["A", "B"],
    "subjects": [
        "math",
        "english",
        "physics",
        "chemistry",
        "biology",
        "history",
        "geography"
    ],
    "assessment_type": [
        {"type": "midterm", "percentage": 30},
        {"type": "final", "percentage": 70},
        {"type": "quiz", "percentage": 10}
    ],
    "semester": 1
}

student_data = {
    "first_name": "Abubeker",
    "father_name": "Abdullahi",
    "g_father_name": "Ibrahim",
    "father_phone": "+2519999999",
    "age": 18,
    "grade": 12,
}


def register_admin(client):
    """Register an admin for testing."""
    unique_email = f"admin-{uuid.uuid4()}@example.com"

    # Register an admin before login
    client.post('/api/v1/admin/registration',
                     data=json.dumps(
                         {"name": "Abdullahi", "email": unique_email, "password": "testpassword"}),
                     content_type='application/json')
    return unique_email


def get_admin_access_token(client):
    """Get the access token for the admin."""
    email = register_admin(client)
    response = client.post('/api/v1/admin/login',
                                data=json.dumps(
                                    {"name": "Abdullahi", "email": email, "password": "testpassword"}),
                                content_type='application/json')

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
                                   data=json.dumps(mark_list_data),
                                   headers={
                                       'Authorization': f'Bearer {token}'},
                                   content_type='application/json')

        if response.status_code != 201:
            raise Exception
    except Exception as e:
        client.fail("Mark list creation failed. Test failed")
    return token


def register_teacher(client):
    """Register an teacher for testing."""
    unique_email = f"teacher-{uuid.uuid4()}@example.com"

    # Register an teacher before login
    client.post('/api/v1/teacher/registration',
                     data=json.dumps(
                         {"name": "Abdullahi", "email": unique_email, "password": "testpassword"}),
                     content_type='application/json')
    return unique_email


def get_teacher_access_token(client):
    """Get the access token for the teacher."""
    email = register_teacher(client)
    response = client.post('/api/v1/teacher/login',
                                data=json.dumps(
                                    {"name": "Abdullahi", "email": email, "password": "testpassword"}),
                                content_type='application/json')

    json_data = response.get_json()
    return json_data['access_token']


def register_student(client):
    """Register a student for testing."""

    # Register a student before login
    response = client.post('/api/v1/student/registration',
                     data=json.dumps(student_data),
                     content_type='application/json')

    return response


def admin_course_assign_to_teacher(client):
    """Test that an admin can access teacher course data."""
    # Test that a valid login returns a token
    try:
        token = create_mark_list(client)
        teacher_token = get_teacher_access_token(client)

        response = client.get('/api/v1/admin/teachers',
                                headers={
                                    'Authorization': f'Bearer {token}'},
                                content_type='application/json')

        if response.status_code != 200:
            raise Exception

        teachers_data = response.json

        random_entry = random.choice(teachers_data)
        teacher_id = random_entry.get('id')

        response = client.put(f'/api/v1/admin/teacher/{teacher_id}/detail/course',
                                data=json.dumps(
                                    {
                                        "grade": 12,
                                        "section": ["A", "B"],
                                        "subject": "math"
                                    }
                                ),
                                headers={
                                    'Authorization': f'Bearer {token}'},
                                content_type='application/json')
    except Exception as e:
        client.fail("Admin course assignment failed. Test failed")

    return teacher_token
