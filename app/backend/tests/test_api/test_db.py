from models.year import Year
from models.table import Table
from models.subject import Subject
from models.grade import Grade


def test_db_grade_count(client, db_session):
    # Query the database
    grade_count = db_session.query(Grade).count()

    # Assert that the database has the correct number of grades
    assert grade_count == 12


def test_db_grade_values(client, db_session):
    # Query the database
    grades = db_session.query(Grade.grade).order_by(Grade.grade).all()
    grade_values = [grade.grade for grade in grades]

    # Assert that the database has the correct grade values
    assert grade_values == list(range(1, 13))


def test_db_subject_count(client, db_session):
    # Query the database
    subject = db_session.query(Subject).count()
    assert subject > 0


def test_db_year_count(client, db_session):
    # Query the database
    year = db_session.query(Year).count()
    assert year > 0


def test_db_table_count(client, db_session):
    # Query the database
    table = db_session.query(Table).count()
    assert table > 0


def test_each_users_registration(client, register_user_temp):
    pass


def test_all_users_registration(client, register_user):
    pass


def test_users_log_in_success(client, users_auth_header):
    pass


def test_teacher_dashboard(client, teacher_auth_header):
    response = client.get(
        "/api/v1/teacher/dashboard", headers=teacher_auth_header["header"]
    )

    assert response.status_code == 200


def test_semester_creation(create_semester):
    pass


def test_available_subjects_for_registration(client, create_semester, stud_auth_header):
    response = client.get(
        "/api/v1/student/course/registration", headers=stud_auth_header["header"]
    )
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert len(response.json) > 0


def test_student_course_registration(stud_course_register):
    pass


def test_get_registered_grades(client, admin_auth_header, stud_course_register):
    response = client.get(
        "/api/v1/admin/registered_grades", headers=admin_auth_header["header"]
    )
    assert response.status_code == 200
    assert "grades" in response.json
    assert isinstance(response.json["grades"], list)
    assert len(response.json["grades"]) > 0


def test_admin_create_mark_list(create_mark_list):
    pass
