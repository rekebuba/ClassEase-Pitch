#!/usr/bin/python3

import unittest
from models.user import User
from models import storage
from api import create_app
from models.student import Student
from tests.test_api.helper_functions import *

class TestEvents(unittest.TestCase):
    """
    Unit tests for the Event-related API endpoints.

    This test suite includes the following tests:

    The tests use a test client to simulate API requests and responses. The `setUp` method initializes the test app and client, 
    while the `tearDown` method cleans up the database after each test.
    """

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

    def test_event_creation_success(self):
        """Test the event creation endpoint for successful registration."""
        
        
        response = create_event(self.client)
        self.assertEqual(response.status_code, 201)
        json_data = response.get_json()
        self.assertIn('event created successfully!', json_data['message'])
