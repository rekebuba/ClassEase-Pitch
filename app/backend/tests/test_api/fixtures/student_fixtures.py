import pytest
from flask.testing import FlaskClient


@pytest.fixture(scope="module")
def stud_course_register(client: FlaskClient, all_stud_auth_header, create_semester):
    for auth_header in all_stud_auth_header:
        get_course = client.get(
            "/api/v1/student/course/registration", headers=auth_header["header"]
        )
        assert get_course.status_code == 200
        courses = get_course.json

        response = client.post(
            "/api/v1/student/course/registration",
            json=courses,
            headers=auth_header["header"],
        )

        # Debugging failed cases
        if response.status_code != 201:
            print(f"Failed for: {courses}")
            print(f"Response: {response.json}")

        assert response.status_code == 201
        assert response.json["message"] == "Course registration successful!"
