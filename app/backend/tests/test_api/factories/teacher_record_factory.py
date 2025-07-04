#!/usr/bin/python3
from factory import SubFactory
from app.backend.models.teacher_record import TeachersRecord
from app.backend.tests.test_api.factories.base_factory import BaseFactory
from app.backend.tests.test_api.factories.academic_term_factory import (
    AcademicTermFactory,
)
from app.backend.tests.test_api.factories.grade_factory import GradeFactory
from app.backend.tests.test_api.factories.section_factory import SectionFactory
from app.backend.tests.test_api.factories.subject_factory import SubjectFactory
from app.backend.tests.test_api.factories.teacher_factory import TeacherFactory


class TeacherRecordFactory(BaseFactory):
    class Meta:
        model = TeachersRecord

    teacher_id = SubFactory(TeacherFactory)
    academic_term_id = SubFactory(AcademicTermFactory)
    subject_id = SubFactory(SubjectFactory)
    grade_id = SubFactory(GradeFactory)
    section_id = SubFactory(SectionFactory)
