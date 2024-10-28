import unittest
from models import storage
from api import create_app
import json
from models.teacher import Teacher
from tests.test_api.helper_functions import *

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
        response = register_teacher(self.client)
        self.assertEqual(response.status_code, 201)
        json_data = response.get_json()
        self.assertIn('Teacher registered successfully!', json_data['message'])

    def test_teacher_login_success(self):
        """Test that the teacher login endpoint works."""
        register_teacher(self.client)
        id = storage.get_random(Teacher).id

        # Test that a valid login returns a token
        response = self.client.get(f'/api/v1/login?id={id}&password={id}',
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.access_token = json_data['access_token']
        self.assertIn('access_token', json_data)

    def test_teacher_login_wrong_id(self):
        # Test that an invalid id returns an error
        id = 'fake'

        # Test that a valid login returns a token
        response = self.client.get(f'/api/v1/login?id={id}&password={id}', content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_admin_login_wrong_password(self):
        # Test that an invalid password returns an error
        register_teacher(self.client)
        id = storage.get_random(Teacher).id
        response = self.client.get(f'/api/v1/login?id={id}&password=wrong', content_type='application/json')
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

    def test_get_teacher_assigned_grade_success(self):
        """Test that the get_teacher_assigned_grade endpoint works."""
        # Assign a grade to the teacher
        teacher_token = admin_course_assign_to_teacher(self.client)

        if not teacher_token:
            self.fail("Admin course assignment failed. Test failed")

        response = self.client.get('/api/v1/teacher/students/assigned_grade',
                                    headers={
                                        'Authorization': f'Bearer {teacher_token}'},
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('grade', json_data)
        self.assertIsInstance(json_data['grade'], list)
        self.assertGreater(len(json_data['grade']), 0)

    def test_get_teacher_assigned_grade_no_grades(self):
        """Test that the get_teacher_assigned_grade endpoint returns 404 if no grades are assigned."""
        # Register a teacher but do not assign any grades
        token = get_teacher_access_token(self.client)

        if not token:
            self.fail("Token not generated. Test failed. Check the login endpoint.")

        response = self.client.get('/api/v1/teacher/students/assigned_grade',
                                    headers={
                                        'Authorization': f'Bearer {token}'},
                                    content_type='application/json')

        self.assertEqual(response.status_code, 404)
        json_data = response.get_json()
        self.assertIn('error', json_data)
        self.assertEqual(json_data['error'], "No grades were assigned")
