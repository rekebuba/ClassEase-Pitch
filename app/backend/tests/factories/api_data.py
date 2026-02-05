import random
import uuid
from typing import get_args

from factory import LazyAttribute
from faker import Faker

from project.api.v1.routers.registrations.schema import (
    EmployeeRegistrationForm,
    StudentRegistrationForm,
)
from project.api.v1.routers.year.schema import NewYear
from project.utils.enum import (
    AcademicTermTypeEnum,
    AcademicYearStatusEnum,
    BloodTypeEnum,
    EmployeePositionEnum,
    ExperienceYearEnum,
    GenderEnum,
    HighestEducationEnum,
    MaritalStatusEnum,
)
from project.utils.type import SetupMethodType
from tests.factories.typed_factory import TypedFactory

fake = Faker()


class NewYearFactory(TypedFactory[NewYear]):
    class Meta:
        model = NewYear

    name = LazyAttribute(lambda _: fake.name())
    calendar_type = LazyAttribute(lambda _: random.choice(list(AcademicTermTypeEnum)))
    start_date = LazyAttribute(lambda _: fake.past_date())
    end_date = LazyAttribute(lambda _: fake.future_date())
    status = LazyAttribute(
        lambda _: random.choice(
            [AcademicYearStatusEnum.ACTIVE, AcademicYearStatusEnum.UPCOMING]
        )
    )
    setup_methods = LazyAttribute(lambda _: random.choice(get_args(SetupMethodType)))
    copy_from_year_id = LazyAttribute(
        lambda x: uuid.uuid4() if x.setup_methods == "Last Year Copy" else None
    )


class StudentRegistrationFactory(TypedFactory[StudentRegistrationForm]):
    class Meta:
        model = StudentRegistrationForm

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


class EmployeeRegistrationFactory(TypedFactory[EmployeeRegistrationForm]):
    class Meta:
        model = EmployeeRegistrationForm

    first_name = LazyAttribute(lambda x: fake.first_name())
    father_name = LazyAttribute(lambda x: fake.last_name())
    grand_father_name = LazyAttribute(lambda x: fake.first_name())
    date_of_birth = LazyAttribute(lambda x: fake.date_of_birth())
    gender = LazyAttribute(lambda x: fake.random_element(elements=list(GenderEnum)))
    nationality = LazyAttribute(lambda x: fake.country())
    marital_status = LazyAttribute(
        lambda x: fake.random_element(elements=list(MaritalStatusEnum))
    )
    social_security_number = LazyAttribute(lambda x: str(fake.uuid4()))
    # Contact Information
    address = LazyAttribute(lambda x: fake.address())
    city = LazyAttribute(lambda x: fake.city())
    state = LazyAttribute(lambda x: fake.state())
    country = LazyAttribute(lambda x: fake.country()[:50])
    primary_phone = LazyAttribute(lambda x: "+251912345678")
    secondary_phone = LazyAttribute(lambda x: "+251912345678")
    personal_email = LazyAttribute(lambda x: fake.email())

    # Emergency Contact
    emergency_contact_name = LazyAttribute(lambda x: fake.name())
    emergency_contact_relation = LazyAttribute(
        lambda x: fake.random_element(
            elements=("Parent", "Sibling", "Spouse", "Friend", "Other")
        )
    )
    emergency_contact_phone = LazyAttribute(lambda x: "+251912345678")
    emergency_contact_email = LazyAttribute(lambda x: fake.email())

    # Educational Background
    highest_education = LazyAttribute(
        lambda x: fake.random_element(elements=list(HighestEducationEnum))
    )

    university = LazyAttribute(lambda x: fake.company())
    graduation_year = LazyAttribute(lambda x: random.randint(2000, 2023))
    gpa = LazyAttribute(lambda x: round(random.uniform(1.0, 4.0), 2))

    # Teaching Experience
    years_of_experience = LazyAttribute(
        lambda x: fake.random_element(elements=list(ExperienceYearEnum))
    )

    # Employment Information
    position = LazyAttribute(
        lambda x: fake.random_element(elements=list(EmployeePositionEnum))
    )
    subject_id = None  # To be set explicitly if position is Teacher

    # Background & References
    reference1_name = LazyAttribute(lambda x: fake.name())
    reference1_organization = LazyAttribute(lambda x: fake.company())
    reference1_phone = LazyAttribute(lambda x: "+251912345678")
    reference1_email = LazyAttribute(lambda x: fake.email())

    # Documents
    resume = LazyAttribute(lambda x: fake.file_name(extension="pdf"))
    agree_to_terms = LazyAttribute(lambda _: True)
    agree_to_background_check = LazyAttribute(lambda _: True)
