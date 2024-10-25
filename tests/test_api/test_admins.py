import unittest
from models import storage
from api import create_app
import json
import random
from models.admin import Admin
from models.users import User
from tests.test_api.helper_functions import register_admin, get_admin_access_token, create_mark_list, get_teacher_access_token, register_teacher, register_student, mark_list_data


class TestAdmin(unittest.TestCase):
    """Test the admin login endpoint."""

    def setUp(self):
        # Create a test app and a test client
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app.app_context().push()

    def tearDown(self):
        # Clean up and drop the tables after each test
        storage.get_session().remove()
        storage.drop_all()

    def test_admin_register_success(self):
        # Test that the admin register endpoint works
        # self.drop_table()
        response = self.client.post('/api/v1/admin/registration',
                                    data=json.dumps(
                                        {"name": "Abdullahi", "email": "newadmin@example.com"}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        json_data = response.get_json()
        self.assertIn('Admin registered successfully!', json_data['message'])

    def test_admin_login_success(self):
        """Test that the admin login endpoint works."""
        register_admin(self.client)

        # Test that a valid login returns a token
        response = self.client.post('/api/v1/login',
                                    data=json.dumps(
                                        {"name": "Abdullahi", "id": storage.get_random(Admin).id, "password": storage.get_random(Admin).id}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.access_token = json_data['access_token']
        self.assertIn('access_token', json_data)

    def test_admin_login_wrong_id(self):
        # Test that an invalid email returns an error
        response = self.client.post('/api/v1/login',
                                    data=json.dumps(
                                        {"name": "Abdullahi", "id": "dose't exist", "password": "testpassword"}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_admin_login_wrong_password(self):
        # Test that an invalid password returns an error
        register_admin(self.client)
        response = self.client.post('/api/v1/login',
                                    data=json.dumps(
                                        {"name": "Abdullahi", "id": storage.get_random(Admin).id, "password": "wrongpassword"}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_admin_dashboard_success(self):
        # Test that a valid login returns a token
        token = get_admin_access_token(self.client)

        if not token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = self.client.get('/api/v1/admin/dashboard',
                                   headers={
                                       'Authorization': f'Bearer {token}'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_admin_dashboard_failure(self):
        # Test that a valid login returns a token
        token = get_admin_access_token(self.client)

        if not token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = self.client.get('/api/v1/admin/dashboard',
                                   headers={
                                       'Authorization': f'Bearer {token}invalid'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 401)

    def test_admin_create_mark_list(self):
        """Test that an admin can create a mark list."""
        # Test that a valid login returns a token
        token = get_admin_access_token(self.client)

        if not token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = register_student(self.client)
        if response.status_code != 201:
            self.fail(
                "Student can not be registered. Test failed. Check the student registration endpoint")

        response = self.client.put('/api/v1/admin/students/mark_list',
                                   data=json.dumps(mark_list_data),
                                   headers={
                                       'Authorization': f'Bearer {token}'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 201)
        json_data = response.get_json()
        self.assertIn('Mark list created successfully!', json_data['message'])

    def test_admin_create_mark_list_failure(self):
        """Test that an admin can create a mark list."""
        # Test that a valid login returns a token
        token = get_admin_access_token(self.client)

        if not token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = self.client.put('/api/v1/admin/students/mark_list',
                                   data=json.dumps(mark_list_data),
                                   headers={
                                       'Authorization': f'Bearer {token}invalid'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 401)

    def test_view_admin_mark_list(self):
        """Test that an admin can view mark list."""
        # Test that a valid login returns a token
        token = create_mark_list(self.client)

        if not token:
            self.fail("Mark list creation failed. Test failed")

        response = self.client.get('/api/v1/admin/students/mark_list?grade=12&section=B&subject=english&semester=1&year=2023/24',
                                   headers={
                                       'Authorization': f'Bearer {token}'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_admin_access_to_teacher_data(self):
        """Test that an admin can access teacher data."""
        # Test that a valid login returns a token
        token = get_admin_access_token(self.client)
        register_teacher(self.client)

        if not token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = self.client.get('/api/v1/admin/teachers',
                                   headers={
                                       'Authorization': f'Bearer {token}'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_admin_access_to_teacher_data_failure(self):
        """Test that an admin can access teacher data."""
        # Test that a valid login returns a token
        token = get_admin_access_token(self.client)

        if not token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = self.client.get('/api/v1/admin/teachers',
                                   headers={
                                       'Authorization': f'Bearer {token}invalid'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 401)

    def test_admin_course_assign_to_teacher(self):
        """Test that an admin can access teacher course data."""
        # Test that a valid login returns a token
        token = create_mark_list(self.client)
        if not token:
            self.fail("Mark list creation failed. Test failed")

        get_teacher_access_token(self.client)

        if not token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = self.client.get('/api/v1/admin/teachers',
                                   headers={
                                       'Authorization': f'Bearer {token}'},
                                   content_type='application/json')

        if response.status_code != 200:
            self.fail("Teacher data not found. Test failed.")

        teachers_data = response.json

        random_entry = random.choice(teachers_data)
        teacher_id = random_entry.get('id')

        response = self.client.put(f'/api/v1/admin/teacher/detail/course?teacher_id={teacher_id}',
                                   data=json.dumps(
                                       {
                                           "grade": 12,
                                           "section": ["A", "B"],
                                           "subject": "math",
                                           "year": "2023/24"
                                       }
                                   ),
                                   headers={
                                       'Authorization': f'Bearer {token}'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 201)

    def test_admin_course_assign_to_teacher_failure(self):
        """Test that an admin can access teacher course data."""
        # Test that a valid login returns a token
        token = create_mark_list(self.client)

        if not token:
            self.fail("Mark list creation failed. Test failed")

        get_teacher_access_token(self.client)

        if not token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = self.client.get('/api/v1/admin/teachers',
                                   headers={
                                       'Authorization': f'Bearer {token}'},
                                   content_type='application/json')

        if response.status_code != 200:
            self.fail("Teacher data not found. Test failed.")

        teachers_data = response.json

        random_entry = random.choice(teachers_data)
        teacher_id = random_entry.get('id')

        response = self.client.put(f'/api/v1/admin/teacher/detail/course?teacher_id={teacher_id}',
                                   data=json.dumps(
                                       {
                                           "grade": 12,
                                           "section": ["A", "B"],
                                           "subject": "math",
                                           "year": "2023/24"
                                       }
                                   ),
                                   headers={
                                       'Authorization': f'Bearer {token}invalid'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 401)
