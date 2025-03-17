#!/usr/bin/python3

import unittest
from models.user import User
from models import storage
from api import create_app
from models.student import Student
from tests.test_api.helper_functions import *

class TestStudents(unittest.TestCase):
    """
    Unit tests for the student-related API endpoints.

    This test suite includes the following tests:
    - `test_student_register_success`: Verifies that the student registration endpoint works correctly.
    - `test_student_login_success`: Ensures that a valid student login returns an access token.
    - `test_student_login_wrong_id`: Checks that an invalid student ID returns an error.
    - `test_student_login_wrong_password`: Ensures that an invalid password returns an error.
    - `test_student_dashboard_success`: Verifies that accessing the student dashboard with a valid token is successful.
    - `test_student_dashboard_failure`: Ensures that accessing the student dashboard with an invalid token returns an error.

    The tests use a test client to simulate API requests and responses. The `setUp` method initializes the test app and client, 
    while the `tearDown` method cleans up the database after each test.
    """
    """Test the student login endpoint."""

    def setUp(self):
        """
        Set up the test environment before each test.

        This method creates a test instance of the application and a test client
        to simulate requests to the application. It also pushes the application
        context to make the app's resources available during the tests.
        """
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app.app_context().push()

    def tearDown(self):
        """
        Tears down the test environment after each test.

        This method is called after each test to clean up the database by removing the session and dropping all tables.
        """
        storage.session.remove()
        storage.drop_all()

    def test_student_register_success(self):
        """
        Test the student registration endpoint for successful registration.

        This test ensures that the student registration endpoint works correctly
        by checking that the response status code is 201 (Created) and that the
        response JSON contains the success message 'Student registered successfully!'.
        """
        response = register_user(self.client, 'student')
        self.assertEqual(response.status_code, 201)
        json_data = response.get_json()
        self.assertIn('student registered successfully!', json_data['message'])

    def test_student_login_success(self):
        """
        Test the student login endpoint for successful login.

        This test ensures that a student can successfully log in using valid credentials.
        It performs the following steps:
        1. Registers a new student.
        2. Retrieves a random student's ID from the storage.
        3. Sends a POST request to the login endpoint with the student's ID and password.
        4. Verifies that the response status code is 200 (OK).
        5. Extracts the access token from the response JSON data.
        6. Asserts that the access token is present in the response.

        Assertions:
        - The response status code should be 200.
        - The response JSON should contain an 'access_token' key.
        """
        register_user(self.client, 'student')
        id = storage.session.query(User).filter_by(role='student').first().identification

        print(id)
        # Test that a valid login returns a token
        response = self.client.post(
            f'/api/v1/auth/login', data=json.dumps({"id": id, "password": id}), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('apiKey', json_data)

    def test_student_login_wrong_id(self):
        """
        Test that an invalid student ID returns an error during login.

        This test verifies that when a student attempts to log in with an invalid
        ID, the API responds with a 401 Unauthorized status code.

        Steps:
        1. Set an invalid student ID.
        2. Attempt to log in using the invalid ID and password.
        3. Assert that the response status code is 401.

        Expected Result:
        The response status code should be 401, indicating that the login attempt
        with an invalid ID is unauthorized.
        """
        id = 'fake'

        # Test that a valid login returns a token
        response = self.client.post(
            f'/api/v1/auth/login', data=json.dumps({"id": id, "password": id}), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_student_login_wrong_password(self):
        """
        Test that an invalid password returns an error.

        This test registers a student and attempts to log in with an incorrect password.
        It verifies that the response status code is 401, indicating unauthorized access.

        Steps:
        1. Register a student using the `register_student` function.
        2. Retrieve a random student's ID from the storage.
        3. Attempt to log in with the retrieved ID and an incorrect password.
        4. Assert that the response status code is 401.

        Expected Result:
        - The login attempt with an incorrect password should return a 401 status code.
        """
        register_user(self.client, 'student')
        id = storage.get_random(Student).id

        response = self.client.post(
            f'/api/v1/login', data=json.dumps({"id": id, "password": 'wrong'}), content_type='application/json')

        self.assertEqual(response.status_code, 401)

    def test_student_dashboard_success(self):
        """
        Test the student dashboard endpoint for successful access.

        This test verifies that a valid login returns a token and that the token
        can be used to access the student dashboard endpoint successfully.

        Steps:
        1. Obtain a valid student access token using the `get_student_access_token` method.
        2. Use the token to make a GET request to the student dashboard endpoint.
        3. Assert that the response status code is 200, indicating successful access.

        Fails if:
        - The token is not generated.
        - The response status code is not 200.
        """
        token = get_student_api_key(self.client)

        if not token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = self.client.get('/api/v1/student/dashboard',
                                   headers={
                                       'apiKey': f'Bearer {token}'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_student_dashboard_failure(self):
        """
        Test the student dashboard access with an invalid token.

        This test ensures that accessing the student dashboard with an invalid 
        token results in a 401 Unauthorized status code.

        Steps:
        1. Obtain a valid student access token.
        2. Append 'invalid' to the token to simulate an invalid token.
        3. Attempt to access the student dashboard with the invalid token.
        4. Verify that the response status code is 401 Unauthorized.

        Asserts:
        - The response status code is 401.
        """
        token = get_student_api_key(self.client)

        if not token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = self.client.get('/api/v1/student/dashboard',
                                   headers={
                                       'apiKey': f'Bearer {token}invalid'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 401)
