import random
from typing import Any, Dict
from factory import LazyAttribute, SubFactory, RelatedFactoryList, SelfAttribute
from faker import Faker
from pyethiodate import EthDate  # type: ignore
from datetime import datetime
from models.student import Student
from models import storage
from tests.test_api.factories.student_year_record_factory import (
    StudentYearRecordFactory,
)
from .base_factory import BaseFactory
from .user_factory import UserFactory
from extension.enums.enum import (
    GenderEnum,
    RoleEnum,
    StudentApplicationStatusEnum,
)

fake = Faker()

StudentYearRecordFactory


class StudentFactory(BaseFactory[Student]):
    class Meta:
        model = Student
        sqlalchemy_session = storage.session
        exclude = ("user",)

    # _add_for_test: Dict[str, Any] = {
    #     "user": lambda **kwarg: UserFactory.build(role=RoleEnum.STUDENT.value),
    #     "grade": lambda **kwarg: random.randint(1, 10),
    #     "academic_year": lambda **kwarg: EthDate.date_to_ethiopian(datetime.now()).year,
    # }

    user: Any = SubFactory(UserFactory, role=RoleEnum.STUDENT)
    student_year_records: Any = RelatedFactoryList(
        "tests.test_api.factories.StudentYearRecordFactory",
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
        lambda x: fake.random_element(
            elements=("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-")
        )
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
