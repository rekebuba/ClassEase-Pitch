#!/usr/bin/python3
from typing import Any
from factory import SubFactory, LazyAttribute
from models.teacher_academic_term_link import TeacherAcademicTermLink
from .base_factory import BaseFactory


class TeacherAcademicTermLinkFactory(BaseFactory[TeacherAcademicTermLink]):
    class Meta:
        model = TeacherAcademicTermLink
        exclude = ("teacher", "academic_term", "section")

    teacher: Any = SubFactory("tests.factories.models.TeacherFactory")
    academic_term: Any = SubFactory(
        "tests.factories.models.academic_term_factory.AcademicTermFactory"
    )

    teacher_id: Any = LazyAttribute(lambda x: x.teacher.id)
    academic_term_id: Any = LazyAttribute(lambda x: x.academic_term.id)
