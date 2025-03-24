#!/usr/bin/python

import unittest
from tests.test_api.factories import *
from tests.test_api.factories_methods import MakeFactory
from models.user import User
from models import storage
from api import create_app
import json
import random
from models.admin import Admin
from tests.test_api.helper_functions import *
from models.base_model import CustomTypes


class TestAdmin(unittest.TestCase):
    """
    TestAdmin is a test suite for testing the admin-related endpoints of the API.

    Methods:
        setUp: Initializes the test app and client before each test.
        tearDown: Cleans up and drops the tables after each test.
        test_admin_register_success: Tests that the admin register endpoint works.
        test_admin_login_success: Tests that the admin login endpoint works.
        test_admin_login_wrong_id: Tests that an invalid ID returns an error.
        test_admin_login_wrong_password: Tests that an invalid password returns an error.
        test_admin_dashboard_success: Tests that a valid login allows access to the admin dashboard.
        test_admin_dashboard_failure: Tests that an invalid token denies access to the admin dashboard.
        test_admin_create_mark_list: Tests that an admin can create a mark list.
        test_admin_create_mark_list_failure: Tests that an invalid token denies mark list creation.
        test_view_admin_mark_list: Tests that an admin can view the mark list.
        test_admin_access_to_teacher_data: Tests that an admin can access teacher data.
        test_admin_access_to_teacher_data_failure: Tests that an invalid token denies access to teacher data.
        test_admin_course_assign_to_teacher: Tests that an admin can assign courses to a teacher.
        test_admin_course_assign_to_teacher_failure: Tests that assigning a non-existent subject returns an error.
    """
    """Test the admin login endpoint."""

    def setUp(self):
        """
        Set up the test environment before each test.

        This method creates a test instance of the application configured for testing,
        initializes a test client for making HTTP requests, and pushes the application
        context to make the app's resources available during the tests.
        """
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app.app_context().push()
        self.session = storage.session

    def tearDown(self):
        """
        Tears down the test environment after each test.

        This method is called after each test to clean up the database by removing the session and dropping all tables.
        """
        storage.session.remove()
        storage.drop_all()

    def test_admin_register_success(self):
        """
        Test the successful registration of an admin.

        This test ensures that the admin register endpoint functions correctly by:
        1. Sending a registration request for an admin.
        2. Verifying that the response status code is 201 (Created).
        3. Checking that the response JSON contains the success message 'Admin registered successfully!'.
        """
        role = CustomTypes.RoleEnum.ADMIN
        user = MakeFactory(UserFactory, self.session, built=True).factory(
            role=role, keep={'id'})

        if 'image_path' in user:
            local_path = user.pop('image_path')
            user['image_path'] = open(local_path, 'rb')
            os.remove(local_path)  # remove the file

        admin = MakeFactory(AdminFactory, self.session, built=True).factory(
            user_id=user.pop('id'))

        response = self.client.post(f'/api/v1/registration/{role.value}',
                                    data={**user, **admin})

        assert response.status_code == 201
        assert response.json['message'] == 'admin registered successfully!'

    def test_admin_login_success(self):
        """
        Test the admin login endpoint for successful login.

        This test performs the following steps:
        1. Registers an admin user.
        2. Retrieves a random admin's ID from the storage.
        3. Sends a POST request to the login endpoint with the admin's ID and password.
        4. Asserts that the response status code is 200 (OK).
        5. Extracts the access token from the response JSON data.
        6. Asserts that the access token is present in the response JSON data.

        The test ensures that a valid login returns an access token.
        """
        """Test that the admin login endpoint works."""
        register_user(self.client, 'admin')
        id = storage.session.query(User).filter_by(
            role='admin').first().identification

        print(id)
        # Test that a valid login returns a token
        response = self.client.post(
            f'/api/v1/auth/login', data=json.dumps({"id": id, "password": id}), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('apiKey', json_data)

    def test_admin_login_wrong_id(self):
        """
        Test that an invalid admin login returns an error.

        This test checks that when an invalid email and password are provided,
        the API returns a 401 Unauthorized status code.

        Steps:
        1. Set an invalid id and password.
        2. Send a POST request to the login endpoint with the invalid credentials.
        3. Assert that the response status code is 401.

        Expected Result:
        The response status code should be 401, indicating unauthorized access.
        """
        id = 'fake'

        # Test that a valid login returns a token
        response = self.client.post(
            f'/api/v1/auth/login', data=json.dumps({"id": id, "password": id}), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_admin_login_wrong_password(self):
        """
        Test the admin login functionality with an incorrect password.

        This test registers an admin, retrieves a random admin's ID from storage, 
        and attempts to log in with an incorrect password. It asserts that the 
        response status code is 401, indicating unauthorized access.

        Steps:
        1. Register an admin using the client.
        2. Retrieve a random admin's ID from storage.
        3. Attempt to log in with the retrieved ID and an incorrect password.
        4. Assert that the response status code is 401.

        Expected Result:
        - The response status code should be 401, indicating that the login attempt 
            with the wrong password is unauthorized.
        """
        register_user(self.client, 'admin')
        id = storage.session.query(User).filter_by(
            role='admin').first().identification
        response = self.client.post(
            f'/api/v1/auth/login', data=json.dumps({"id": id, "password": 'wrong'}), content_type='application/json')

        self.assertEqual(response.status_code, 401)

    def test_admin_dashboard_success(self):
        """
        Test the admin dashboard access with a valid login.

        This test verifies that a valid login returns a token and that the token
        can be used to access the admin dashboard endpoint successfully.

        Steps:
        1. Obtain an admin access token using the `get_admin_api_key` method.
        2. If the token is not generated, the test fails with an appropriate message.
        3. Use the token to make a GET request to the admin dashboard endpoint.
        4. Assert that the response status code is 200, indicating successful access.

        Raises:
            AssertionError: If the token is not generated or the response status code is not 200.
        """
        token = get_admin_api_key(self.client)

        if not token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = self.client.get('/api/v1/admin/dashboard',
                                   headers={
                                       'apiKey': f'Bearer {token}'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_admin_dashboard_failure(self):
        """
        Test the admin dashboard access with an invalid token.

        This test ensures that accessing the admin dashboard with an invalid token
        returns a 401 Unauthorized status code.

        Steps:
        1. Obtain a valid admin access token.
        2. Append 'invalid' to the token to simulate an invalid token.
        3. Attempt to access the admin dashboard with the invalid token.
        4. Verify that the response status code is 401 Unauthorized.

        Assertions:
        - The response status code should be 401, indicating unauthorized access.
        """
        token = get_admin_api_key(self.client)

        if not token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = self.client.get('/api/v1/admin/dashboard',
                                   headers={
                                       'apiKey': f'Bearer {token}invalid'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 401)

    def test_admin_create_mark_list(self):
        """
        Test the creation of a mark list by an admin.

        This test case verifies that an admin can successfully create a mark list for a student.
        It performs the following steps:
        1. Obtains an admin access token by logging in.
        2. Registers a student.
        3. Generates mark list data.
        4. Sends a PUT request to create the mark list for the registered student.
        5. Asserts that the response status code is 201 (Created).
        6. Asserts that the response message indicates successful creation of the mark list.

        Raises:
            AssertionError: If the token is not generated, student registration fails, or mark list creation fails.
        """
        token = get_admin_api_key(self.client)

        if not token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = register_user(self.client, 'student')
        if response.status_code != 201:
            self.fail(
                "Student can not be registered. Test failed. Check the student registration endpoint")

        mark_list = generate_mark_list_data()
        response = self.client.put('/api/v1/admin/students/mark_list',
                                   data=json.dumps(mark_list),
                                   headers={
                                       'apiKey': f'Bearer {token}'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 201)
        json_data = response.get_json()
        self.assertIn('Mark list created successfully!', json_data['message'])

    def test_admin_create_mark_list_failure(self):
        """
        Test case for creating a mark list with invalid token.

        This test ensures that the API returns a 401 Unauthorized status code
        when an attempt is made to create a mark list with an invalid token.

        Steps:
        1. Obtain an admin access token.
        2. Attempt to create a mark list with an invalid token.
        3. Verify that the response status code is 401.

        Asserts:
        - The response status code is 401 Unauthorized.
        """
        token = get_admin_api_key(self.client)

        if not token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = self.client.put('/api/v1/admin/students/mark_list',
                                   data=json.dumps(generate_mark_list_data()),
                                   headers={
                                       'apiKey': f'Bearer {token}invalid'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 401)

    def test_view_admin_mark_list(self):
        """
        Test that an admin can view the mark list for students.

        This test ensures that an admin, after successfully logging in and obtaining a token,
        can retrieve the mark list for students of a specific grade and academic year.

        Steps:
        1. Create a mark list and obtain a valid token.
        2. Use the token to make a GET request to the endpoint for viewing the mark list.
        3. Verify that the response status code is 200, indicating success.

        Raises:
            AssertionError: If the mark list creation fails or the response status code is not 200.
        """
        token = create_mark_list(self.client)

        if not token:
            self.fail("Mark list creation failed. Test failed")

        response = self.client.get('/api/v1/admin/manage/students?grade=1&year=2024/25',
                                   headers={
                                       'apiKey': f'Bearer {token}'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_admin_access_to_teacher_data(self):
        """
        Test that an admin can access teacher data.

        This test performs the following steps:
        1. Obtains an admin access token by calling `get_admin_api_key`.
        2. Registers a teacher using `register_teacher`.
        3. Verifies that the token is generated; if not, the test fails.
        4. Sends a GET request to the `/api/v1/admin/teachers` endpoint with the token.
        5. Asserts that the response status code is 200, indicating successful access to teacher data.
        """
        token = get_admin_api_key(self.client)
        register_user(self.client, 'teacher')

        if not token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = self.client.get('/api/v1/admin/teachers',
                                   headers={
                                       'apiKey': f'Bearer {token}'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_admin_access_to_teacher_data_failure(self):
        """
        Test case to verify that an admin cannot access teacher data with an invalid token.

        This test attempts to access the teacher data endpoint using an invalid token
        and expects a 401 Unauthorized response.

        Steps:
        1. Obtain an admin access token.
        2. Append 'invalid' to the token to simulate an invalid token.
        3. Make a GET request to the '/api/v1/admin/teachers' endpoint with the invalid token.
        4. Assert that the response status code is 401.

        Expected Result:
        The response status code should be 401, indicating unauthorized access.
        """
        token = get_admin_api_key(self.client)

        if not token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = self.client.get('/api/v1/admin/teachers',
                                   headers={
                                       'apiKey': f'Bearer {token}invalid'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 401)

    def test_admin_course_assign_to_teacher(self):
        """
        Test case for assigning a course to a teacher by an admin.

        This test performs the following steps:
        1. Creates a mark list and retrieves the token.
        2. Retrieves a teacher access token.
        3. Fetches the list of teachers using the admin token.
        4. Randomly selects a teacher from the list.
        5. Assigns the selected teacher to a course with specified details.
        6. Asserts that the assignment was successful and the response contains the expected message.

        The test will fail if:
        - The mark list creation fails.
        - The teacher access token is not generated.
        - The teacher data is not found.
        - The assignment response status code is not 201.
        - The response message does not contain 'Teacher assigned successfully!'.
        """
        token = create_mark_list(self.client)
        if not token:
            self.fail("Mark list creation failed. Test failed")

        teacher_token = get_teacher_api_key(self.client)

        if not teacher_token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = self.client.get('/api/v1/admin/teachers',
                                   headers={
                                       'apiKey': f'Bearer {token}'},
                                   content_type='application/json')

        if response.status_code != 200:
            self.fail("Teacher data not found. Test failed.")

        teachers_data = response.json

        random_entry = random.choice(teachers_data['teachers'])
        teacher_id = random_entry.get('id')

        response = self.client.put(f'/api/v1/admin/assign-teacher',
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
                                       'apiKey': f'Bearer {token}'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 201)
        json_data = response.get_json()
        self.assertIn('Teacher assigned successfully!', json_data['message'])

    def test_admin_course_assign_to_teacher_failure(self):
        """
        Test that an admin cannot assign a non-existent subject to a teacher.

        This test verifies that the system prevents an admin from assigning a subject 
        that does not exist to a teacher. It ensures that the appropriate error message 
        and status code are returned when attempting to assign an invalid subject.

        Steps:
        1. Create a mark list and obtain a token.
        2. Obtain a teacher access token.
        3. Retrieve the list of teachers.
        4. Select a random teacher from the list.
        5. Attempt to assign a non-existent subject to the selected teacher.
        6. Verify that the response status code is 404.
        7. Verify that the error message 'Subject not found' is present in the response.

        Raises:
            AssertionError: If any of the steps fail or the expected response is not received.
        """
        token = create_mark_list(self.client)
        if not token:
            self.fail("Mark list creation failed. Test failed")

        teacher_token = get_teacher_api_key(self.client)

        if not teacher_token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = self.client.get('/api/v1/admin/teachers',
                                   headers={
                                       'apiKey': f'Bearer {token}'},
                                   content_type='application/json')

        if response.status_code != 200:
            self.fail("Teacher data not found. Test failed.")

        teachers_data = response.json

        random_entry = random.choice(teachers_data['teachers'])
        teacher_id = random_entry.get('id')

        response = self.client.put(f'/api/v1/admin/assign-teacher',
                                   data=json.dumps(
                                       {
                                           "teacher_id": teacher_id,
                                           "grade": 1,
                                           "section": ["A", "B"],
                                           "subjects_taught": ["dose not exist"],
                                           "mark_list_year": "2024/25"
                                       }
                                   ),
                                   headers={
                                       'apiKey': f'Bearer {token}'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)
        json_data = response.get_json()
        self.assertIn('Subject not found', json_data['error'])
