from typing import Any, Dict
import pytest
from sqlalchemy import select
from sqlmodel import col
from models.student import Student
from tests.test_api.factories import (
    AvailableSubject,
    MarkListFactory,
)
from models.subject import Subject
from models.grade import Grade
from models import storage
from sqlalchemy.orm import scoped_session, Session


@pytest.fixture(scope="session")
def fake_mark_list(db_session: scoped_session[Session]) -> Dict[str, Any]:
    # generate fake mark list for each grade
    stmt = (
        select(Grade)
        .join(Student)
        .where(Grade.id == Student.current_grade_id, col(Student.is_registered))
        .group_by(Grade.id)
    )
    registered_grades = db_session.execute(stmt).all()

    grades = {grade.grade for grade in registered_grades}
    mark_list = MarkListFactory(grade_num=len(grades)).to_dict()
    mark_list.pop("grade_num")

    for grade, assessment in zip(list(grades), mark_list["mark_assessment"]):
        assessment["grade"] = grade
        new_stmt = select(Subject.name)
        subjects = db_session.execute(new_stmt).all()
        custom_subjects = [
            AvailableSubject(subject=name, subject_code=code, grade=assessment["grade"])
            for name, code in subjects
        ]
        assessment["subjects"] = custom_subjects

    return mark_list
