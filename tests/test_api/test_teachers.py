import unittest
from models import storage
from api import create_app
import json
from models.teacher import Teacher
from tests.test_api.helper_functions import register_teacher, get_teacher_access_token, create_mark_list, admin_course_assign_to_teacher

class TestTeachers(unittest.TestCase):
    """Test the teacher login endpoint."""
    def setUp(self):
        # Create a test app and a test client
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app.app_context().push()

    def tearDown(self):
        # Clean up and drop the tables after each test
        storage.get_session().remove()
        storage.drop_all()

    def test_teacher_register_success(self):
        # Test that the teacher register endpoint works
        response = self.client.post('/api/v1/teacher/registration',
                                    data=json.dumps(
                                        {"name": "Abdullahi", "email": "newteacher@example.com"}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        json_data = response.get_json()
        self.assertIn('Teacher registered successfully!', json_data['message'])

    def test_teacher_login_success(self):
        """Test that the teacher login endpoint works."""
        email = register_teacher(self.client)

        # Test that a valid login returns a token
        response = self.client.post('/api/v1/teacher/login',
                                    data=json.dumps(
                                        {"email": email, "password": storage.get_random(Teacher).id}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.access_token = json_data['access_token']
        self.assertIn('access_token', json_data)

    def test_teacher_login_wrong_email(self):
        # Test that an invalid email returns an error
        response = self.client.post('/api/v1/teacher/login',
                                    data=json.dumps(
                                        {"name": "Abdullahi", "email": "dose't exist", "password": "testpassword"}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_teacher_login_wrong_password(self):
        # Test that an invalid password returns an error
        email = register_teacher(self.client)
        response = self.client.post('/api/v1/teacher/login',
                                    data=json.dumps(
                                        {"name": "Abdullahi", "email": email, "password": "wrongpassword"}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_teacher_dashboard_success(self):
        # Test that a valid login returns a token
        token = get_teacher_access_token(self.client)

        if not token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = self.client.get('/api/v1/teacher/dashboard',
                                   headers={
                                       'Authorization': f'Bearer {token}'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_teacher_dashboard_failure(self):
        # Test that a valid login returns a token
        token = get_teacher_access_token(self.client)

        if not token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = self.client.get('/api/v1/teacher/dashboard',
                                   headers={
                                       'Authorization': f'Bearer {token}invalid'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 401)

    def test_view_teacher_mark_list(self):
        """Test that an admin can view mark list."""
        # Test that a valid login returns a token
        teacher_token = admin_course_assign_to_teacher(self.client)

        if not teacher_token:
            self.fail("Admin course assignment failed. Test failed")

        response = self.client.get('/api/v1/teacher/students/mark_list?grade=12&section=A&semester=1&school_year=2023/24',
                                      headers={
                                        'Authorization': f'Bearer {teacher_token}'},
                                      content_type='application/json')

        self.assertEqual(response.status_code, 200)
