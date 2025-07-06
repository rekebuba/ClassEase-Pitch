from typing import Any
from factory import LazyAttribute, SubFactory, SelfAttribute
from models.assessment import Assessment
from .base_factory import BaseFactory


class AssessmentFactory(BaseFactory[Assessment]):
    class Meta:
        model = Assessment
        exclude = ("student", "student_term_record", "yearly_subject")

    student: Any = SubFactory(
        "tests.test_api.factories.StudentFactory", student_year_records=[]
    )
    student_term_record: Any = SubFactory(
        "tests.test_api.factories.StudentTermRecordFactory",
        student=SelfAttribute("..student"),
        assessments=[],
    )
    yearly_subject: Any = SubFactory(
        "tests.test_api.factories.YearlySubjectFactory",
    )

    student_id: Any = LazyAttribute(lambda x: x.student.id)
    student_term_record_id: Any = LazyAttribute(
        lambda x: x.student_term_record.id
    )
    yearly_subject_id: Any = LazyAttribute(lambda x: x.yearly_subject.id)
