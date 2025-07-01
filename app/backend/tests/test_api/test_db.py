from sqlalchemy import select
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
    grade_count = db_session.execute(select(Grade)).all()

    # Assert that the database has the correct number of grades
    assert len(grade_count) == 12


def test_db_grade_values(
    client: FlaskClient, db_session: scoped_session[Session]
) -> None:
    # Query the database
    grades = db_session.scalars(select(Grade).order_by(Grade.grade)).all()
    grade_values = [grade.grade for grade in grades]

    # Assert that the database has the correct grade values
    assert grade_values == list(range(1, 13))


def test_db_subject_count(
    client: FlaskClient, db_session: scoped_session[Session]
) -> None:
    # Query the database
    subject = db_session.execute(select(Subject)).all()
    assert len(subject) > 0


def test_db_year_count(
    client: FlaskClient, db_session: scoped_session[Session]
) -> None:
    # Query the database
    year = db_session.execute(select(Year)).all()
    assert len(year) > 0


def test_db_table_count(
    client: FlaskClient, db_session: scoped_session[Session]
) -> None:
    # Query the database
    table = db_session.execute(select(Table)).all()
    assert len(table) > 0
