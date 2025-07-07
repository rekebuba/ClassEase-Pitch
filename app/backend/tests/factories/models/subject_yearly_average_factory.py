from typing import Any
from factory import LazyAttribute, SubFactory, SelfAttribute
from faker import Faker
from models.subject_yearly_average import SubjectYearlyAverage
from .base_factory import BaseFactory

fake = Faker()


class SubjectYearlyAverageFactory(BaseFactory[SubjectYearlyAverage]):
    class Meta:
        model = SubjectYearlyAverage
        exclude = ("student", "student_year_record", "yearly_subject")

    student: Any = SubFactory(
        "tests.factories.models.StudentFactory", student_year_records=[]
    )
    student_year_record: Any = SubFactory(
        "tests.factories.models.StudentYearRecordFactory",
        student=SelfAttribute("..student"),
        student_term_records=[],
    )
    yearly_subject: Any = SubFactory(
        "tests.factories.models.YearlySubjectFactory",
    )

    student_id: Any = LazyAttribute(lambda x: x.student.id)
    yearly_subject_id: Any = LazyAttribute(lambda x: x.yearly_subject.id)
    student_year_record_id: Any = LazyAttribute(lambda x: x.student_year_record.id)

    average: Any = LazyAttribute(lambda _: None)
    rank: Any = LazyAttribute(lambda _: None)
