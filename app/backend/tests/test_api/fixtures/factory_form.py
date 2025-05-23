import pytest
from tests.test_api.factories_methods import MakeFactory
from models.student import Student
from tests.test_api.factories import (
    AvailableSubject,
    DefaultFelids,
    EventFactory,
    MarkListFactory,
    SemesterFactory,
)
from models.subject import Subject
from models.grade import Grade
from models import storage


@pytest.fixture(scope="module")
def event_form(db_session):
    event = MakeFactory(EventFactory, db_session, built=True).factory(
        purpose="New Semester", add={"academic_year": DefaultFelids.current_EC_year()}
    )
    form = MakeFactory(SemesterFactory, db_session, built=True).factory()

    semester_form = {
        **event,
        "semester": {**form},
    }

    return semester_form


@pytest.fixture(scope="module")
def fake_mark_list(db_session):
    # generate fake mark list for each grade
    registered_grades = (
        storage.session.query(Grade)
        .join(Student, Student.current_grade_id == Grade.id)
        .filter(Student.is_registered)
        .group_by(Grade.id)
        .all()
    )

    grades = {grade.grade for grade in registered_grades}
    mark_list = MarkListFactory(grade_num=len(grades)).to_dict()
    mark_list.pop("grade_num")

    for grade, assessment in zip(list(grades), mark_list["mark_assessment"]):
        assessment["grade"] = grade
        subjects = (
            db_session.query(Subject.name, Subject.code)
            .join(Grade, Grade.id == Subject.grade_id)
            .filter(Grade.grade == assessment["grade"])
            .all()
        )
        custom_subjects = [
            AvailableSubject(subject=name, subject_code=code, grade=assessment["grade"])
            for name, code in subjects
        ]
        assessment["subjects"] = custom_subjects

    return mark_list
