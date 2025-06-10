from models.year import Year
from models.table import Table
from models.subject import Subject
from models.grade import Grade
from flask.testing import FlaskClient
from sqlalchemy.orm import scoped_session, Session


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
