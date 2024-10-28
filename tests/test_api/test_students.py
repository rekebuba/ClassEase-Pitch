import unittest
from models import storage
from api import create_app
from models.student import Student
from tests.test_api.helper_functions import *

class TestStudents(unittest.TestCase):
    """Test the student login endpoint."""

    def setUp(self):
        # Create a test app and a test client
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app.app_context().push()

    def tearDown(self):
        # Clean up and drop the tables after each test
        storage.get_session().remove()
        storage.drop_all()

    def test_student_register_success(self):
        # Test that the student register endpoint works
        response = register_student(self.client)
        self.assertEqual(response.status_code, 201)
        json_data = response.get_json()
        self.assertIn('Student registered successfully!', json_data['message'])

    def test_student_login_success(self):
        """Test that the student login endpoint works."""
        register_student(self.client)
        id = storage.get_random(Student).id
        # Test that a valid login returns a token
        response = self.client.get(f'/api/v1/login?id={id}&password={id}', content_type='application/json')

        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.access_token = json_data['access_token']
        self.assertIn('access_token', json_data)

    def test_student_login_wrong_id(self):
        # Test that an invalid email returns an error
        id = 'fake'

        # Test that a valid login returns a token
        response = self.client.get(f'/api/v1/login?id={id}&password={id}', content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_student_login_wrong_password(self):
        # Test that an invalid password returns an error
        register_student(self.client)
        id = storage.get_random(Student).id

        response = self.client.get(f'/api/v1/login?id={id}&password=wrong', content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_student_dashboard_success(self):
        # Test that a valid login returns a token
        token = get_student_access_token(self.client)

        if not token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = self.client.get('/api/v1/student/dashboard',
                                   headers={
                                       'Authorization': f'Bearer {token}'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_student_dashboard_failure(self):
        # Test that a valid login returns a token
        token = get_student_access_token(self.client)

        if not token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = self.client.get('/api/v1/student/dashboard',
                                   headers={
                                       'Authorization': f'Bearer {token}invalid'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 401)
