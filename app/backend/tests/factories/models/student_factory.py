from typing import Any
from factory import LazyAttribute, SubFactory, RelatedFactoryList
from faker import Faker
from models.student import Student
from tests.factories.models.grade_factory import GradeFactory
from .base_factory import BaseFactory
from .user_factory import UserFactory
from extension.enums.enum import (
    BloodTypeEnum,
    GenderEnum,
    RoleEnum,
    StudentApplicationStatusEnum,
)

fake = Faker()


class StudentFactory(BaseFactory[Student]):
    class Meta:
        model = Student
        exclude = ("user", "starting_grade")

    user: Any = SubFactory(
        "tests.factories.models.user_factory.UserFactory",
        role=RoleEnum.STUDENT,
    )
    user_id: Any = LazyAttribute(lambda x: x.user.id if x.user else None)
    starting_grade: Any = LazyAttribute(lambda _: GradeFactory.create())
    starting_grade_id: Any = LazyAttribute(lambda x: x.starting_grade.id)
    student_year_records: Any = RelatedFactoryList(
        "tests.factories.models.StudentYearRecordFactory",
        factory_related_name="student",
        size=1,
    )

    # Personal Information
    first_name: Any = LazyAttribute(lambda x: fake.first_name())
    father_name: Any = LazyAttribute(lambda x: fake.last_name())
    grand_father_name: Any = LazyAttribute(lambda x: fake.first_name())
    date_of_birth: Any = LazyAttribute(lambda x: fake.date_of_birth(minimum_age=6))
    gender: Any = LazyAttribute(
        lambda x: fake.random_element(elements=list(GenderEnum))
    )
    nationality: Any = LazyAttribute(lambda x: fake.country())
    blood_type: Any = LazyAttribute(
        lambda x: fake.random_element(elements=list(BloodTypeEnum))
    )
    student_photo: Any = LazyAttribute(lambda x: fake.file_name(extension="jpg"))

    # Academic Information
    is_transfer: Any = LazyAttribute(lambda x: fake.boolean())
    previous_school: Any = LazyAttribute(
        lambda obj: fake.company() if obj.is_transfer else None
    )
    previous_grades: Any = LazyAttribute(
        lambda obj: fake.text() if obj.is_transfer else None
    )
    transportation: Any = LazyAttribute(
        lambda x: fake.random_element(elements=("Bus", "Walk", "Parent"))
    )

    # Contact Information
    address: Any = LazyAttribute(lambda x: fake.address())
    city: Any = LazyAttribute(lambda x: fake.city())
    state: Any = LazyAttribute(lambda x: fake.state())
    postal_code: Any = LazyAttribute(lambda x: fake.postcode())
    father_phone: Any = LazyAttribute(lambda x: "091234567")
    mother_phone: Any = LazyAttribute(lambda x: "091234567")
    parent_email: Any = LazyAttribute(lambda x: fake.email())

    # Guardian Information
    guardian_name: Any = LazyAttribute(lambda x: fake.name())
    guardian_phone: Any = LazyAttribute(lambda x: "091234567")
    guardian_relation: Any = LazyAttribute(
        lambda x: fake.random_element(elements=("Parent", "Sibling", "Other"))
    )
    emergency_contact_name: Any = LazyAttribute(lambda x: fake.name())
    emergency_contact_phone: Any = LazyAttribute(lambda x: "091234567")
    sibling_in_school: Any = LazyAttribute(lambda x: fake.boolean())
    sibling_details: Any = LazyAttribute(
        lambda obj: fake.text() if obj.sibling_in_school else None
    )

    # Medical Information
    has_medical_condition: Any = LazyAttribute(lambda _: fake.boolean())
    medical_details: Any = LazyAttribute(
        lambda obj: fake.text(max_nb_chars=60) if obj.has_medical_condition else None
    )
    has_disability: Any = LazyAttribute(lambda x_: fake.boolean())
    disability_details: Any = LazyAttribute(
        lambda obj: fake.text(max_nb_chars=60) if obj.has_disability else None
    )
    status: Any = LazyAttribute(lambda x: StudentApplicationStatusEnum.PENDING)
