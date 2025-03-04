import unittest
from models.user import User
from models import storage
from api import create_app
import json
from models.teacher import Teacher
from tests.test_api.helper_functions import *

class TestTeachers(unittest.TestCase):
    """
    TestTeachers is a test case class for testing the teacher-related endpoints of the API.

    Methods:
        setUp(): Set up the test environment before each test.
        tearDown(): Clean up the test environment after each test.
        test_teacher_register_success(): Test that the teacher register endpoint works and returns a 201 status code.
        test_teacher_login_success(): Test that the teacher login endpoint works and returns a valid access token.
        test_teacher_login_wrong_id(): Test that an invalid teacher ID returns a 401 status code.
        test_admin_login_wrong_password(): Test that an invalid password returns a 401 status code.
        test_teacher_dashboard_success(): Test that a valid login allows access to the teacher dashboard and returns a 200 status code.
        test_teacher_dashboard_failure(): Test that an invalid token prevents access to the teacher dashboard and returns a 401 status code.
        test_get_teacher_assigned_grade_success(): Test that the get_teacher_assigned_grade endpoint works and returns a list of grades.
        test_get_teacher_assigned_grade_no_grades(): Test that the get_teacher_assigned_grade endpoint returns a 404 status code if no grades are assigned.
    """
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

    def tearDown(self):
        """
        Tears down the test environment after each test.

        This method is called after each test to clean up the database by removing the session and dropping all tables.
        """
        storage.session.remove()
        storage.drop_all()

    def test_teacher_register_success(self):
        """
        Test the successful registration of a teacher.

        This test ensures that the teacher registration endpoint functions correctly
        by verifying that a successful registration returns a status code of 201 and
        includes a success message in the response JSON.

        Steps:
        1. Call the `register_teacher` function with the test client.
        2. Assert that the response status code is 201.
        3. Parse the response JSON.
        4. Assert that the response JSON contains the success message.

        """
        response = register_user(self.client, 'teacher')
        self.assertEqual(response.status_code, 201)
        json_data = response.get_json()
        self.assertIn('teacher registered successfully!', json_data['message'])

    def test_teacher_login_success(self):
        """
        Test the teacher login endpoint for successful login.

        This test registers a teacher, retrieves a random teacher's ID from storage,
        and attempts to log in using that ID as both the username and password.
        It verifies that the login is successful by checking the response status code
        and ensuring that an access token is included in the response.

        Steps:
        1. Register a teacher.
        2. Retrieve a random teacher's ID.
        3. Attempt to log in using the teacher's ID as both the username and password.
        4. Verify that the response status code is 200 (OK).
        5. Check that the response contains an access token.

        Assertions:
        - The response status code should be 200.
        - The response should contain an 'ApiKey' key.
        """
        register_user(self.client, 'teacher')
        id = storage.session.query(User).filter_by(role='teacher').first().identification

        print(id)
        # Test that a valid login returns a token
        response = self.client.post(
            f'/api/v1/auth/login', data=json.dumps({"id": id, "password": id}), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('apiKey', json_data)

    def test_teacher_login_wrong_id(self):
        """
        Test that an invalid teacher ID returns an error during login.

        This test simulates a login attempt with an invalid teacher ID and 
        verifies that the response status code is 401 (Unauthorized).

        Steps:
        1. Set an invalid teacher ID.
        2. Attempt to login using the invalid ID and password.
        3. Assert that the response status code is 401.

        Expected Result:
        - The login attempt should fail, returning a 401 status code.
        """
        # Test that an invalid id returns an error
        id = 'fake'

        # Test that a valid login returns a token
        response = self.client.post(
            f'/api/v1/auth/login', data=json.dumps({"id": id, "password": id}), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_admin_login_wrong_password(self):
        """
        Test that an invalid password returns an error during admin login.

        This test registers a teacher, retrieves a random teacher's ID, and attempts to log in with an incorrect password.
        It asserts that the response status code is 401, indicating unauthorized access.

        Steps:
        1. Register a teacher using the `register_teacher` function.
        2. Retrieve a random teacher's ID from the storage.
        3. Attempt to log in with the retrieved ID and an incorrect password.
        4. Assert that the response status code is 401.

        Expected Result:
        - The login attempt with an incorrect password should return a 401 Unauthorized status code.
        """
        register_user(self.client, 'teacher')
        id = storage.get_random(Teacher).id
        response = self.client.post(
            f'/api/v1/login', data=json.dumps({"id": id, "password": "wrong"}), content_type='application/json')

        self.assertEqual(response.status_code, 401)

    def test_teacher_dashboard_success(self):
        """
        Test the teacher dashboard endpoint for successful access.

        This test verifies that a valid login returns a token and that the 
        token can be used to access the teacher dashboard endpoint successfully.

        Steps:
        1. Obtain a valid access token using the `get_teacher_ApiKey` method.
        2. Ensure the token is generated; otherwise, fail the test.
        3. Use the token to make a GET request to the teacher dashboard endpoint.
        4. Verify that the response status code is 200, indicating success.

        Raises:
            AssertionError: If the token is not generated or the response status 
                            code is not 200.
        """
        # Test that a valid login returns a token
        token = get_teacher_api_key(self.client)

        if not token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = self.client.get('/api/v1/teacher/dashboard',
                                   headers={
                                       'Authorization': f'Bearer {token}'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_teacher_dashboard_failure(self):
        """
        Test the teacher dashboard access with an invalid token.

        This test ensures that accessing the teacher dashboard with an invalid
        token results in a 401 Unauthorized status code.

        Steps:
        1. Obtain a valid teacher access token.
        2. Modify the token to make it invalid.
        3. Attempt to access the teacher dashboard with the invalid token.
        4. Verify that the response status code is 401 Unauthorized.

        Asserts:
        - The response status code is 401.
        """
        token = get_teacher_api_key(self.client)

        if not token:
            self.fail(
                "Token not generated. Test failed. Check the login endpoint.")

        response = self.client.get('/api/v1/teacher/dashboard',
                                   headers={
                                       'Authorization': f'Bearer {token}invalid'},
                                   content_type='application/json')

        self.assertEqual(response.status_code, 401)

    def test_get_teacher_assigned_grade_success(self):
        """
        Test the successful retrieval of a teacher's assigned grade.

        This test verifies that the `get_teacher_assigned_grade` endpoint functions correctly by:
        1. Assigning a grade to a teacher using the `admin_course_assign_to_teacher` helper function.
        2. Sending a GET request to the `/api/v1/teacher/students/assigned_grade` endpoint with the teacher's token.
        3. Checking that the response status code is 200 (OK).
        4. Ensuring the response JSON contains a 'grade' key.
        5. Verifying that the 'grade' key maps to a list.
        6. Confirming that the list of grades is not empty.

        If the grade assignment fails, the test will fail with an appropriate message.
        """
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
        """
        Test the get_teacher_assigned_grade endpoint when no grades are assigned to a teacher.

        This test case verifies that the endpoint returns a 404 status code and an appropriate error message
        when a teacher has no grades assigned. It performs the following steps:
        1. Registers a teacher without assigning any grades.
        2. Generates an access token for the teacher.
        3. Sends a GET request to the /api/v1/teacher/students/assigned_grade endpoint with the generated token.
        4. Asserts that the response status code is 404.
        5. Asserts that the response contains an error message indicating that no grades were assigned.

        Raises:
            AssertionError: If the token is not generated or if the response does not meet the expected conditions.
        """
        token = get_teacher_api_key(self.client)

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
