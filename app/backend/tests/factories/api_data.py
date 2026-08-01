import random
import uuid
from typing import get_args

from factory import LazyAttribute
from faker import Faker

from project.api.v1.routers.auth.route import SchoolAwareOAuth2PasswordRequestForm
from project.api.v1.routers.auth.schema import SignUpRequest
from project.api.v1.routers.employee.schema import EmployeePositionCreate
from project.api.v1.routers.registrations.schema import (
    AdminRegistration,
    EmployeeRegistrationForm,
    ParentRegistrationForm,
    StudentRegistrationForm,
)
from project.api.v1.routers.school.schema import (
    EmployeeProfile,
    NewSchool,
    NewSchoolMembership,
    StudentProfile,
)
from project.api.v1.routers.teachers.schema import CreateTeacherProfile
from project.api.v1.routers.year.schema import NewYear
from project.utils.enum import (
    AcademicTermTypeEnum,
    AcademicYearStatusEnum,
    BloodTypeEnum,
    EmployeePositionEnum,
    EmploymentStatusEnum,
    EmploymentTypeEnum,
    ExperienceYearEnum,
    GenderEnum,
    HighestEducationEnum,
    MaritalStatusEnum,
    RoleEnum,
    SchoolStatusEnum,
)
from project.utils.type import SetupMethodType
from tests.factories.typed_factory import TypedFactory

fake = Faker()


class NewSchoolFactory(TypedFactory[NewSchool]):
    class Meta:
        model = NewSchool

    name = LazyAttribute(lambda _: fake.company())
    slug = LazyAttribute(lambda _: fake.slug(value=fake.company()))
    status = LazyAttribute(lambda _: random.choice(list(SchoolStatusEnum)))
    domain = LazyAttribute(lambda _: fake.domain_name())
    logo_path = LazyAttribute(lambda _: fake.file_name(extension="png"))
    primary_color = LazyAttribute(lambda _: fake.color_name())
    settings = LazyAttribute(lambda _: {"default_language": random.choice(["en", "es", "fr"])})


class SignUpFactory(TypedFactory[SignUpRequest]):
    class Meta:
        model = SignUpRequest

    first_name = LazyAttribute(lambda _: fake.first_name())
    father_name = LazyAttribute(lambda _: fake.last_name())
    grand_father_name = LazyAttribute(lambda _: fake.last_name())
    email = LazyAttribute(lambda _: fake.email())
    phone = LazyAttribute(lambda _: "+251912345678")
    date_of_birth = LazyAttribute(lambda _: fake.date_of_birth(minimum_age=6))
    gender = LazyAttribute(lambda _: random.choice(list(GenderEnum)))
    username = LazyAttribute(lambda _: fake.user_name())
    password = LazyAttribute(lambda _: fake.password(length=12))


class LoginFactory(TypedFactory[SchoolAwareOAuth2PasswordRequestForm]):
    class Meta:
        model = SchoolAwareOAuth2PasswordRequestForm

    username = LazyAttribute(lambda _: fake.user_name())
    password = LazyAttribute(lambda _: fake.password(length=12))
    school_slug = LazyAttribute(lambda _: fake.slug())


class NewSchoolMembershipFactory(TypedFactory[NewSchoolMembership]):
    class Meta:
        model = NewSchoolMembership

    user_id = LazyAttribute(lambda _: uuid.uuid4())
    role = LazyAttribute(lambda _: random.choice(list(RoleEnum)))


class StudentProfileFactory(TypedFactory[StudentProfile]):
    class Meta:
        model = StudentProfile

    user_id = LazyAttribute(lambda _: uuid.uuid4())
    city = LazyAttribute(lambda _: fake.city())
    state = LazyAttribute(lambda _: fake.state())
    postal_code = LazyAttribute(lambda _: fake.postcode())
    nationality = LazyAttribute(lambda _: fake.country())
    blood_type = LazyAttribute(lambda _: random.choice(list(BloodTypeEnum)))
    student_photo = LazyAttribute(lambda _: fake.file_name(extension="jpg"))
    previous_school = LazyAttribute(lambda _: fake.company() if random.choice([True, False]) else None)
    transportation = LazyAttribute(lambda _: random.choice(["Bus", "Walk", "Parent"]))
    has_medical_condition = LazyAttribute(lambda _: random.choice([True, False]))
    disability_details = None
    medical_details = None
    has_medical_condition = False
    has_disability = False
    is_transfer = False


class EmployeeProfileFactory(TypedFactory[EmployeeProfile]):
    class Meta:
        model = EmployeeProfile

    user_id = LazyAttribute(lambda _: uuid.uuid4())
    employee_number = LazyAttribute(lambda _: str(fake.random_number(digits=5)))
    hire_date = LazyAttribute(lambda _: fake.past_date())
    employment_status = LazyAttribute(lambda _: random.choice(list(EmploymentStatusEnum)))
    employment_type = LazyAttribute(lambda _: random.choice(list(EmploymentTypeEnum)))
    termination_date = LazyAttribute(lambda _: fake.future_date() if random.choice([True, False]) else None)
    department_id = LazyAttribute(lambda _: uuid.uuid4())
    primary_position_id = LazyAttribute(lambda _: uuid.uuid4())
    manager_employee_id = LazyAttribute(lambda _: uuid.uuid4())
    work_email = LazyAttribute(lambda _: fake.company_email())
    work_phone = LazyAttribute(lambda _: "+251912345678")


class EmployeePositionFactory(TypedFactory[EmployeePositionCreate]):
    class Meta:
        model = EmployeePositionCreate

    employee_id = LazyAttribute(lambda _: uuid.uuid4())
    position_id = LazyAttribute(lambda _: uuid.uuid4())
    start_date = LazyAttribute(lambda _: fake.past_date())
    end_date = LazyAttribute(lambda _: fake.future_date() if random.choice([True, False]) else None)
    is_primary = LazyAttribute(lambda _: random.choice([True, False]))


class TeacherProfileFactory(TypedFactory[CreateTeacherProfile]):
    class Meta:
        model = CreateTeacherProfile

    employee_id = LazyAttribute(lambda _: uuid.uuid4())
    specialization = LazyAttribute(lambda _: fake.job())
    teacher_license_number = LazyAttribute(lambda _: str(fake.random_number(digits=8)))
    certifications = LazyAttribute(lambda _: fake.sentence(nb_words=5))
    highest_education = LazyAttribute(lambda _: random.choice(list(HighestEducationEnum)))
    years_of_experience = LazyAttribute(lambda _: random.randint(1, 20))


class NewYearFactory(TypedFactory[NewYear]):
    class Meta:
        model = NewYear

    name = LazyAttribute(lambda _: fake.name())
    calendar_type = LazyAttribute(lambda _: random.choice(list(AcademicTermTypeEnum)))
    start_date = LazyAttribute(lambda _: fake.past_date())
    end_date = LazyAttribute(lambda _: fake.future_date())
    status = LazyAttribute(lambda _: random.choice([AcademicYearStatusEnum.ACTIVE, AcademicYearStatusEnum.UPCOMING]))
    setup_methods = LazyAttribute(lambda _: random.choice(get_args(SetupMethodType)))
    copy_from_year_id = LazyAttribute(lambda x: uuid.uuid4() if x.setup_methods == "Last Year Copy" else None)


class AdminRegistrationFactory(TypedFactory[AdminRegistration]):
    class Meta:
        model = AdminRegistration

    first_name = LazyAttribute(lambda x: fake.first_name())
    father_name = LazyAttribute(lambda x: fake.last_name())
    grand_father_name = LazyAttribute(lambda x: fake.first_name())
    date_of_birth = LazyAttribute(lambda x: fake.date_of_birth())
    gender = LazyAttribute(lambda x: fake.random_element(elements=list(GenderEnum)))
    email = LazyAttribute(lambda x: fake.email())
    phone = LazyAttribute(lambda x: "+251912345678")
    username = LazyAttribute(lambda x: fake.user_name())
    password = LazyAttribute(lambda x: fake.password(length=12))


class ParentRegistrationFactory(TypedFactory[ParentRegistrationForm]):
    class Meta:
        model = ParentRegistrationForm

    first_name = LazyAttribute(lambda x: fake.first_name())
    last_name = LazyAttribute(lambda x: fake.last_name())
    gender = LazyAttribute(lambda x: fake.random_element(elements=list(GenderEnum)))
    email = LazyAttribute(lambda x: fake.email())
    phone = LazyAttribute(lambda x: "+251912345678")
    relation = LazyAttribute(lambda x: fake.random_element(elements=("Father", "Mother", "Guardian")))
    emergency_contact_phone = LazyAttribute(lambda x: "+251912345678")


class StudentRegistrationFactory(TypedFactory[StudentRegistrationForm]):
    class Meta:
        model = StudentRegistrationForm

    # To be set explicitly
    registered_for_grade_id = None
    parent_id = None

    # Personal Information
    first_name = LazyAttribute(lambda x: fake.first_name())
    father_name = LazyAttribute(lambda x: fake.last_name())
    grand_father_name = LazyAttribute(lambda x: fake.first_name())
    date_of_birth = LazyAttribute(lambda x: fake.date_of_birth(minimum_age=6))
    gender = LazyAttribute(lambda x: fake.random_element(elements=list(GenderEnum)))
    nationality = LazyAttribute(lambda x: fake.country())
    blood_type = LazyAttribute(lambda x: fake.random_element(elements=list(BloodTypeEnum)))
    student_photo = LazyAttribute(lambda x: fake.file_name(extension="jpg"))

    # Academic Information
    is_transfer = LazyAttribute(lambda x: fake.boolean())
    previous_school = LazyAttribute(lambda obj: fake.company() if obj.is_transfer else None)
    transportation = LazyAttribute(lambda x: fake.random_element(elements=("Bus", "Walk", "Parent")))

    # Contact Information
    city = LazyAttribute(lambda x: fake.city())
    state = LazyAttribute(lambda x: fake.state())
    postal_code = LazyAttribute(lambda x: fake.postcode())

    # Guardian Information
    emergency_contact_name = LazyAttribute(lambda x: fake.name())
    emergency_contact_phone = LazyAttribute(lambda x: "+251912345678")

    # Medical Information
    has_medical_condition = LazyAttribute(lambda _: fake.boolean())
    medical_details = LazyAttribute(lambda obj: fake.text(max_nb_chars=60) if obj.has_medical_condition else None)
    has_disability = LazyAttribute(lambda x_: fake.boolean())
    disability_details = LazyAttribute(lambda obj: fake.text(max_nb_chars=60) if obj.has_disability else None)


class EmployeeRegistrationFactory(TypedFactory[EmployeeRegistrationForm]):
    class Meta:
        model = EmployeeRegistrationForm

    first_name = LazyAttribute(lambda x: fake.first_name())
    father_name = LazyAttribute(lambda x: fake.last_name())
    grand_father_name = LazyAttribute(lambda x: fake.first_name())
    date_of_birth = LazyAttribute(lambda x: fake.date_of_birth())
    gender = LazyAttribute(lambda x: fake.random_element(elements=list(GenderEnum)))
    nationality = LazyAttribute(lambda x: fake.country())
    marital_status = LazyAttribute(lambda x: fake.random_element(elements=list(MaritalStatusEnum)))
    social_security_number = LazyAttribute(lambda x: str(fake.uuid4()))
    # Contact Information
    city = LazyAttribute(lambda x: fake.city())
    state = LazyAttribute(lambda x: fake.state())
    country = LazyAttribute(lambda x: fake.country()[:50])
    phone = LazyAttribute(lambda x: "+251912345678")
    secondary_phone = LazyAttribute(lambda x: "+251912345678")
    email = LazyAttribute(lambda x: fake.email())

    # Emergency Contact
    emergency_contact_name = LazyAttribute(lambda x: fake.name())
    emergency_contact_relation = LazyAttribute(
        lambda x: fake.random_element(elements=("Parent", "Sibling", "Spouse", "Friend", "Other"))
    )
    emergency_contact_phone = LazyAttribute(lambda x: "+251912345678")

    # Educational Background
    highest_education = LazyAttribute(lambda x: fake.random_element(elements=list(HighestEducationEnum)))

    university = LazyAttribute(lambda x: fake.company())
    graduation_year = LazyAttribute(lambda x: random.randint(2000, 2023))
    gpa = LazyAttribute(lambda x: round(random.uniform(1.0, 4.0), 2))

    # Teaching Experience
    years_of_experience = LazyAttribute(lambda x: fake.random_element(elements=list(ExperienceYearEnum)))

    # Employment Information
    position = LazyAttribute(lambda x: fake.random_element(elements=list(EmployeePositionEnum)))
    subject_id = None  # To be set explicitly if position is Teacher

    # Documents
    resume = LazyAttribute(lambda x: fake.file_name(extension="pdf"))
    agree_to_terms = LazyAttribute(lambda _: True)
    agree_to_background_check = LazyAttribute(lambda _: True)
