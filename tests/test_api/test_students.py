import unittest
from models import storage
from api import create_app
import json
from tests.test_api.helper_functions import student_data

class TestStudents(unittest.TestCase):
    """Test the student login endpoint."""

    def setUp(self):
        # Create a test app and a test client
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app.app_context().push()

        self.access_token = None  # Initialize the access token variable

    def tearDown(self):
        # Clean up and drop the tables after each test
        storage.get_session().remove()
        storage.drop_all()

    # def get_student_access_token(self):
    #     """Get the access token for the student."""
    #     response = self.client.post('/api/v1/student/login',
    #                                 data=json.dumps({}),
    #                                 content_type='application/json')

    #     json_data = response.get_json()
    #     return json_data['access_token']

    def test_student_register_success(self):
        # Test that the student register endpoint works
        response = self.client.post('/api/v1/student/registration',
                                    data=json.dumps(student_data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        json_data = response.get_json()
        self.assertIn('Student registered successfully!', json_data['message'])

    # def test_student_login_success(self):
    #     """Test that the student login endpoint works."""
    #     email = self.register_student()

    #     # Test that a valid login returns a token
    #     response = self.client.post('/api/v1/student/login',
    #                                 data=json.dumps(
    #                                     {"email": email, "password": "testpassword"}),
    #                                 content_type='application/json')

    #     self.assertEqual(response.status_code, 200)
    #     json_data = response.get_json()
    #     self.access_token = json_data['access_token']
    #     self.assertIn('access_token', json_data)

    # def test_student_login_wrong_email(self):
    #     # Test that an invalid email returns an error
    #     response = self.client.post('/api/v1/student/login',
    #                                 data=json.dumps(
    #                                     {"first_name": "Abdullahi", "email": "dose't exist", "password": "testpassword"}),
    #                                 content_type='application/json')
    #     self.assertEqual(response.status_code, 401)

    # def test_student_login_wrong_password(self):
    #     # Test that an invalid password returns an error
    #     email = self.register_student()
    #     response = self.client.post('/api/v1/student/login',
    #                                 data=json.dumps(
    #                                     {"first_name": "Abdullahi", "email": email, "password": "wrongpassword"}),
    #                                 content_type='application/json')
    #     self.assertEqual(response.status_code, 401)

    # def test_student_dashboard_success(self):
    #     # Test that a valid login returns a token
    #     token = self.get_student_access_token()

    #     if not token:
    #         self.fail(
    #             "Token not generated. Test failed. Check the login endpoint.")

    #     response = self.client.get('/api/v1/student/dashboard',
    #                                headers={
    #                                    'Authorization': f'Bearer {token}'},
    #                                content_type='application/json')

    #     self.assertEqual(response.status_code, 200)

    # def test_student_dashboard_failure(self):
    #     # Test that a valid login returns a token
    #     token = self.get_student_access_token()

    #     if not token:
    #         self.fail(
    #             "Token not generated. Test failed. Check the login endpoint.")

    #     response = self.client.get('/api/v1/student/dashboard',
    #                                headers={
    #                                    'Authorization': f'Bearer {token}invalid'},
    #                                content_type='application/json')

    #     self.assertEqual(response.status_code, 401)
