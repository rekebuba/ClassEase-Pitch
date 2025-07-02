import random
from typing import Any
from factory import LazyAttribute, SubFactory, RelatedFactoryList, SelfAttribute
from models.student_semester_record import StudentSemesterRecord
from .base_factory import BaseFactory


class StudentSemesterRecordFactory(BaseFactory[StudentSemesterRecord]):
    class Meta:
        model = StudentSemesterRecord
        exclude = ("student", "semester", "section", "student_year_record")

    student: Any = SubFactory(
        "tests.test_api.factories.StudentFactory", student_year_records=[]
    )
    semester: Any = SubFactory("tests.test_api.factories.SemesterFactory")
    section: Any = SubFactory(
        "tests.test_api.factories.SectionFactory", student_semester_records=[]
    )

    student_year_record: Any = SubFactory(
        "tests.test_api.factories.StudentYearRecordFactory",
        student_semester_records=[],
    )

    assessments: Any = RelatedFactoryList(
        "tests.test_api.factories.AssessmentFactory",
        factory_related_name="student_semester_record",
        student=SelfAttribute("..student"),
        size=1,
    )

    student_id: Any = LazyAttribute(lambda x: x.student.id)
    semester_id: Any = LazyAttribute(lambda x: x.semester.id)
    section_id: Any = LazyAttribute(lambda x: x.section.id)
    student_year_record_id: Any = LazyAttribute(lambda x: x.student_year_record.id)

    average: Any = LazyAttribute(lambda _: random.uniform(40.0, 100.0))
    rank: Any = LazyAttribute(lambda _: random.randint(1, 50))
