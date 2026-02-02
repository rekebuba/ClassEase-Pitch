from factory import LazyAttribute, SubFactory
from faker import Faker

from project.models.student import Student
from tests.factories.typed_factory import TypedFactory
from project.utils.enum import (
    BloodTypeEnum,
    GenderEnum,
    RoleEnum,
    StudentApplicationStatusEnum,
)

fake = Faker()


class StudentFactory(TypedFactory[Student]):
    class Meta:
        model = Student
        exclude = ("user",)

    user = SubFactory(
        "tests.factories.models.user_factory.UserFactory",
        role=RoleEnum.STUDENT,
    )

    user_id = LazyAttribute(lambda x: x.user.id if x.user else None)
    registered_for_grade_id = None  # To be set explicitly

    # Personal Information
    first_name = LazyAttribute(lambda x: fake.first_name())
    father_name = LazyAttribute(lambda x: fake.last_name())
    grand_father_name = LazyAttribute(lambda x: fake.first_name())
    date_of_birth = LazyAttribute(lambda x: fake.date_of_birth(minimum_age=6))
    gender = LazyAttribute(lambda x: fake.random_element(elements=list(GenderEnum)))
    nationality = LazyAttribute(lambda x: fake.country())
    blood_type = LazyAttribute(
        lambda x: fake.random_element(elements=list(BloodTypeEnum))
    )
    student_photo = LazyAttribute(lambda x: fake.file_name(extension="jpg"))

    # Academic Information
    is_transfer = LazyAttribute(lambda x: fake.boolean())
    previous_school = LazyAttribute(
        lambda obj: fake.company() if obj.is_transfer else None
    )
    previous_grades = LazyAttribute(
        lambda obj: fake.text() if obj.is_transfer else None
    )
    transportation = LazyAttribute(
        lambda x: fake.random_element(elements=("Bus", "Walk", "Parent"))
    )

    # Contact Information
    address = LazyAttribute(lambda x: fake.address())
    city = LazyAttribute(lambda x: fake.city())
    state = LazyAttribute(lambda x: fake.state())
    postal_code = LazyAttribute(lambda x: fake.postcode())
    father_phone = LazyAttribute(lambda x: "+251912345678")
    mother_phone = LazyAttribute(lambda x: "+251912345678")
    parent_email = LazyAttribute(lambda x: fake.email())

    # Guardian Information
    guardian_name = LazyAttribute(lambda x: fake.name())
    guardian_phone = LazyAttribute(lambda x: "+251912345678")
    guardian_relation = LazyAttribute(
        lambda x: fake.random_element(elements=("Parent", "Sibling", "Other"))
    )
    emergency_contact_name = LazyAttribute(lambda x: fake.name())
    emergency_contact_phone = LazyAttribute(lambda x: "+251912345678")
    sibling_in_school = LazyAttribute(lambda x: fake.boolean())
    sibling_details = LazyAttribute(
        lambda obj: fake.text() if obj.sibling_in_school else None
    )

    # Medical Information
    has_medical_condition = LazyAttribute(lambda _: fake.boolean())
    medical_details = LazyAttribute(
        lambda obj: fake.text(max_nb_chars=60) if obj.has_medical_condition else None
    )
    has_disability = LazyAttribute(lambda x_: fake.boolean())
    disability_details = LazyAttribute(
        lambda obj: fake.text(max_nb_chars=60) if obj.has_disability else None
    )
    status = LazyAttribute(lambda x: StudentApplicationStatusEnum.PENDING)
