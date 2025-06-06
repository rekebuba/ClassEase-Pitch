from typing import List
from models.year import Year
from models.table import Table
from models.subject import Subject
from models.grade import Grade
from flask.testing import FlaskClient
from sqlalchemy.orm import scoped_session, Session
from tests.typing import Credential


def test_db_grade_count(
    client: FlaskClient, db_session: scoped_session[Session]
) -> None:
    # Query the database
    grade_count = db_session.query(Grade).count()

    # Assert that the database has the correct number of grades
    assert grade_count == 12


def test_db_grade_values(
    client: FlaskClient, db_session: scoped_session[Session]
) -> None:
    # Query the database
    grades = db_session.query(Grade.grade).order_by(Grade.grade).all()
    grade_values = [grade.grade for grade in grades]

    # Assert that the database has the correct grade values
    assert grade_values == list(range(1, 13))


def test_db_subject_count(
    client: FlaskClient, db_session: scoped_session[Session]
) -> None:
    # Query the database
    subject = db_session.query(Subject).count()
    assert subject > 0


def test_db_year_count(
    client: FlaskClient, db_session: scoped_session[Session]
) -> None:
    # Query the database
    year = db_session.query(Year).count()
    assert year > 0


def test_db_table_count(
    client: FlaskClient, db_session: scoped_session[Session]
) -> None:
    # Query the database
    table = db_session.query(Table).count()
    assert table > 0


def test_each_user_registration(client: FlaskClient, register_user_temp: None) -> None:
    pass


def test_all_users_registration(
    client: FlaskClient,
    register_admin: None,
    register_teacher: None,
    register_student: None,
) -> None:
    pass


def test_users_log_in_success(
    client: FlaskClient, users_auth_header: List[Credential]
) -> None:
    pass


def test_teacher_dashboard(
    client: FlaskClient, teacher_auth_header: Credential
) -> None:
    response = client.get(
        "/api/v1/teacher/dashboard", headers=teacher_auth_header["header"]
    )

    assert response.status_code == 200


def test_users_dashboard_information(
    client: FlaskClient, users_auth_header: List[Credential]
) -> None:
    response = client.get("/api/v1/", headers=users_auth_header[0]["header"])
    assert response.status_code == 200
    assert response.json is not None
    assert "user" in response.json
    assert isinstance(response.json["user"], dict)
    assert "imagePath" in response.json["user"]
    assert "role" in response.json["user"]
    assert "identification" in response.json["user"]
    assert "detail" in response.json
    assert isinstance(response.json["detail"], dict)
    assert "firstName" in response.json["detail"]
    assert "fatherName" in response.json["detail"]
    assert "grandFatherName" in response.json["detail"]


def test_semester_creation(create_semester: None) -> None:
    pass


def test_available_subjects_for_registration(
    client: FlaskClient, create_semester: None, stud_auth_header: Credential
) -> None:
    response = client.get(
        "/api/v1/student/course/registration", headers=stud_auth_header["header"]
    )
    assert response.status_code == 200
    assert hasattr(response, "json")
    assert isinstance(response.json, dict)
    assert len(response.json) > 0


def test_student_course_registration(
    client: FlaskClient, stud_course_register: None
) -> None:
    pass


def test_get_registered_grades(
    client: FlaskClient,
    stud_course_register: None,
    admin_auth_header: Credential,
) -> None:
    response = client.get(
        "/api/v1/admin/registered_grades", headers=admin_auth_header["header"]
    )
    assert response.status_code == 200
    assert response.json is not None
    assert "grades" in response.json
    assert isinstance(response.json["grades"], list)
    assert len(response.json["grades"]) > 0


def test_admin_create_mark_list(create_mark_list: None) -> None:
    pass


def test_admin_query_students(
    client: FlaskClient,
    # create_mark_list: None,
    admin_auth_header: Credential,
) -> None:
    response = client.post(
        "/api/v1/admin/students", json={}, headers=admin_auth_header["header"]
    )
    assert response.status_code == 200
    assert response.json is not None

    search_params = {
        "join_operator": "or",
        "filters": [
            {
                "tableId": response.json["tableId"]["grade"],
                "id": "grade",
                "variant": "multiSelect",
                "operator": "in",
                "value": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            },
            {
                "tableId": response.json["tableId"]["identification"],
                "id": "identification",
                "variant": "text",
                "operator": "iLike",
                "value": "MAS/1234/56",
            },
            {
                "tableId": response.json["tableId"]["sectionSemesterOne"],
                "id": "sectionSemesterOne",
                "variant": "multiSelect",
                "operator": "in",
                "value": ["A", "B"],
            },
            {
                "tableId": response.json["tableId"][
                    "firstName_fatherName_grandFatherName"
                ],
                "id": "firstName_fatherName_grandFatherName",
                "variant": "text",
                "operator": "iLike",
                "value": "asdfdsfsdfs",
            },
        ],
        "sort": [
            {
                "id": "grade",
                "desc": False,
                "tableId": response.json["tableId"]["grade"],
            },
            {"id": "sectionSemesterOne", "desc": True},
        ],
        "page": 1,
        "per_page": 10,
    }

    response = client.post(
        "/api/v1/admin/students",
        json=search_params,
        headers=admin_auth_header["header"],
    )
    assert response.status_code == 200
    assert response.json is not None
    assert "data" in response.json
    assert isinstance(response.json["data"], list)
    assert len(response.json["data"]) == 0


def test_admin_student_section_counts(
    db_session: scoped_session[Session],
    client: FlaskClient,
    admin_auth_header: Credential,
) -> None:
    response = client.get(
        "/api/v1/admin/students/section-counts",
        headers=admin_auth_header["header"],
    )
    assert response.status_code == 200
    assert response.json is not None
    assert "sectionSemesterOne" in response.json
    assert "sectionSemesterTwo" in response.json
    assert isinstance(response.json["sectionSemesterOne"], dict)
    assert isinstance(response.json["sectionSemesterTwo"], dict)


def test_admin_student_grade_counts(
    db_session: scoped_session[Session],
    client: FlaskClient,
    admin_auth_header: Credential,
) -> None:
    response = client.get(
        "/api/v1/admin/students/grade-counts",
        headers=admin_auth_header["header"],
    )
    assert response.status_code == 200
    assert response.json is not None
