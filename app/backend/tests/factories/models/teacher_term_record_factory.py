import random
from typing import Any
from factory import LazyAttribute, SubFactory
from models.teacher_term_record import TeacherTermRecord
from .base_factory import BaseFactory


class TeacherTermRecordFactory(BaseFactory[TeacherTermRecord]):
    class Meta:
        model = TeacherTermRecord
        exclude = ("teacher", "academic_term", "subject", "section", "grade", "stream")

    teacher: Any = SubFactory("tests.factories.models.TeacherFactory", years=[])
    academic_term: Any = SubFactory("tests.factories.models.AcademicTermFactory")
    subject: Any = SubFactory("tests.factories.models.SubjectFactory")
    section: Any = SubFactory("tests.factories.models.SectionFactory")

    teacher_id: Any = LazyAttribute(lambda x: x.teacher.id)
    academic_term_id: Any = LazyAttribute(lambda x: x.academic_term.id)
    subject_id: Any = LazyAttribute(lambda x: x.subject.id)
    grade_id: Any = LazyAttribute(lambda x: random.choice(x.subject.grades).id)
    stream_id: Any = LazyAttribute(
        lambda x: random.choice(x.subject.streams).id if x.subject.streams else None
    )
    section_id: Any = LazyAttribute(lambda x: x.section.id)
