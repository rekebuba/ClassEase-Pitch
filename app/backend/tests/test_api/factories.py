from datetime import datetime, timedelta
import os
import random
import uuid
import bcrypt
import factory
from faker import Faker
import requests
from pyethiodate import EthDate
from models.year import Year
from models.semester import Semester
from models.teacher import Teacher
from models.student import Student
from models.admin import Admin
from models.user import User
from models.event import Event

fake = Faker()


def remove_fields(form, *args):
    """Removes fields from a form."""
    exclude_fields = {'id', 'created_at', 'updated_at',
                      'sqlalchemy_session', '__class__',
                      'year', 'start_year_id', 'current_year_id',
                      'identification', 'password', 'semester_id',
                      'event_id'}
    data = {key: value for key, value in form.__dict__.items(
    ) if key not in exclude_fields}

    for arg in args:
        data[arg] = {key: value for key, value in form.arg.__dict__.items(
        ) if key not in exclude_fields}

    return data


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = None

    @staticmethod
    def get_ai_profile_picture():
        url = "https://thispersondoesnotexist.com"
        response = requests.get(url)
        if response.status_code == 200:
            directory = "profiles"
            os.makedirs(directory, exist_ok=True)  # Ensure directory exists

            file_name = f"{directory}/{str(fake.uuid4())}.jpg"
            with open(file_name, "wb") as f:
                f.write(response.content)

            return file_name  # Returns the saved file path
        return None

    @staticmethod
    def _generate_id(role):
        """
        Generates a custom ID based on the role (Admin, Student, Teacher).

        The ID format is: <section>/<random_number>/<year_suffix>
        - Section: 'MAS' for Student, 'MAT' for Teacher, 'MAA' for Admin
        - Random number: A 4-digit number between 1000 and 9999
        - Year suffix: Last 2 digits of the current Ethiopian year
        """
        identification = ''
        section = ''

        # Assign prefix based on role
        if role == 'student':
            section = 'MAS'
        elif role == 'teacher':
            section = 'MAT'
        elif role == 'admin':
            section = 'MAA'

        num = random.randint(1000, 9999)
        starting_year = EthDate.date_to_ethiopian(
            datetime.now()).year % 100  # Get last 2 digits of the year
        identification = f'{section}/{num}/{starting_year}'

        return identification

    @staticmethod
    def _hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # image_path = factory.LazyAttribute(
    #     lambda x: UserFactory.get_ai_profile_picture())
    national_id = factory.LazyAttribute(lambda x: str(fake.uuid4()))
    role = factory.LazyAttribute(lambda x: '')
    identification = factory.LazyAttribute(
        lambda obj: UserFactory._generate_id(obj.role))
    password = factory.LazyAttribute(
        lambda obj: UserFactory._hash_password(obj.identification))

    @factory.post_generation
    def clean_data(self, create, extracted, **kwargs):
        """Post-generation hook to clean up data."""
        if not create:
            return

        return remove_fields(self)


class AdminFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Admin
        sqlalchemy_session = None

    user = factory.SubFactory(
        UserFactory, sqlalchemy_session=Meta.sqlalchemy_session, role='admin')
    user_id = factory.LazyAttribute(lambda obj: obj.user.id)
    role = factory.LazyAttribute(lambda obj: obj.user.role)

    # Add additional fields for Admin
    first_name = factory.LazyAttribute(lambda x: fake.first_name())
    father_name = factory.LazyAttribute(lambda x: fake.last_name())
    grand_father_name = factory.LazyAttribute(lambda x: fake.first_name())
    date_of_birth = factory.LazyAttribute(lambda x: fake.date_of_birth())
    email = factory.LazyAttribute(lambda x: fake.email())
    gender = factory.LazyAttribute(
        lambda x: fake.random_element(elements=('M', 'F')))
    phone = factory.LazyAttribute(lambda x: '091234567')
    address = factory.LazyAttribute(lambda x: fake.address())

    @factory.post_generation
    def clean_data(self, create, extracted, **kwargs):
        """Post-generation hook to clean up data."""
        if not create:
            return

        return remove_fields(self, 'user')


class StudentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Student
        sqlalchemy_session = None

    @staticmethod
    def current_EC_year() -> int:
        return EthDate.date_to_ethiopian(datetime.now()).year

    user = factory.SubFactory(
        UserFactory, sqlalchemy_session=Meta.sqlalchemy_session, role='student')
    user_id = factory.LazyAttribute(lambda obj: obj.user.id)
    role = factory.LazyAttribute(lambda obj: obj.user.role)

    # Add additional fields for Admin
    first_name = factory.LazyAttribute(lambda x: fake.first_name())
    father_name = factory.LazyAttribute(lambda x: fake.last_name())
    grand_father_name = factory.LazyAttribute(lambda x: fake.first_name())
    date_of_birth = factory.LazyAttribute(lambda x: fake.date_of_birth())
    gender = factory.LazyAttribute(
        lambda x: fake.random_element(elements=('M', 'F')))
    father_phone = factory.LazyAttribute(lambda x: '091234567')
    mother_phone = factory.LazyAttribute(lambda x: '091234567')
    guardian_name = factory.LazyAttribute(lambda x: fake.name())
    guardian_phone = factory.LazyAttribute(lambda x: '091234567')

    academic_year = factory.LazyAttribute(
        lambda x: StudentFactory.current_EC_year())

    # Allow start_year_id and current_year_id to be passed explicitly
    start_year_id = factory.SelfAttribute('start_year.id')
    current_year_id = factory.SelfAttribute('current_year.id')

    is_transfer = factory.LazyAttribute(lambda x: fake.boolean())
    previous_school_name = factory.LazyAttribute(
        lambda obj: fake.company() if obj.is_transfer else '')

    current_grade = factory.LazyAttribute(lambda x: random.randint(1, 12))
    # semester_id = factory.LazyAttribute(lambda x: str(fake.uuid4()))
    has_passed = factory.LazyAttribute(lambda x: False)
    next_grade = factory.LazyAttribute(lambda x: None)
    is_registered = factory.LazyAttribute(lambda x: False)

    has_medical_condition = factory.LazyAttribute(lambda _: fake.boolean())
    medical_details = factory.LazyAttribute(
        lambda obj: fake.text() if obj.has_medical_condition else '')
    has_disability = factory.LazyAttribute(lambda x_: fake.boolean())
    disability_details = factory.LazyAttribute(
        lambda obj: fake.text() if obj.has_disability else '')
    requires_special_accommodation = factory.LazyAttribute(
        lambda _: fake.boolean())
    special_accommodation_details = factory.LazyAttribute(
        lambda obj: fake.text() if obj.requires_special_accommodation else ''
    )

    is_active = factory.LazyAttribute(lambda x: True)

    @factory.post_generation
    def clean_data(self, create, extracted, **kwargs):
        """Post-generation hook to clean up data."""
        if not create:
            return

        return remove_fields(self, 'user', 'year')


class TeacherFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Teacher
        sqlalchemy_session = None

    user = factory.SubFactory(
        UserFactory, sqlalchemy_session=Meta.sqlalchemy_session, role='teacher')

    user_id = factory.LazyAttribute(lambda obj: obj.user.id)
    role = factory.LazyAttribute(lambda obj: obj.user.role)

    # Add additional fields for Teacher
    first_name = factory.LazyAttribute(lambda x: fake.first_name())
    father_name = factory.LazyAttribute(lambda x: fake.last_name())
    grand_father_name = factory.LazyAttribute(lambda x: fake.first_name())
    date_of_birth = factory.LazyAttribute(lambda x: fake.date_of_birth())
    email = factory.LazyAttribute(lambda x: fake.email())
    gender = factory.LazyAttribute(lambda x: fake.random_element(
        elements=('M', 'F')))
    phone = factory.LazyAttribute(lambda x: '091234567')
    address = factory.LazyAttribute(lambda x: fake.address())
    year_of_experience = factory.LazyAttribute(lambda x: random.randint(0, 5))
    qualification = factory.LazyAttribute(lambda x: fake.random_element(
        elements=('Certified Teacher', 'Diploma in Education', 'Degree in Education')))

    @factory.post_generation
    def clean_data(self, create, extracted, **kwargs):
        """Post-generation hook to clean up data."""
        if not create:
            return

        return remove_fields(self, 'user')


class EventFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Event
        sqlalchemy_session = None

    title = factory.LazyAttribute(lambda x: fake.sentence())
    purpose = factory.LazyAttribute(lambda x: fake.random_element(
        elements=('New Semester', 'Graduation',
                  'Sports Event', 'Administration', 'Other')
    ))
    organizer = factory.LazyAttribute(lambda obj: fake.random_element(
        elements=('School Administration', 'School',
                  'Student Club', 'External Organizer')
    ) if obj.purpose != 'New Semester' else 'School Administration'
    )

    academic_year = factory.LazyAttribute(
        lambda x: EthDate.date_to_ethiopian(datetime.now()).year)

    start_date = factory.LazyAttribute(lambda x: fake.past_date())
    end_date = factory.LazyAttribute(lambda x: fake.future_date())
    start_time = factory.LazyAttribute(
        lambda x: datetime.now() - timedelta(hours=1))  # Past datetime
    end_time = factory.LazyAttribute(
        lambda x: datetime.now() + timedelta(hours=1))  # Future datetime

    location_type = factory.LazyAttribute(
        lambda obj: fake.random_element(
            elements=('Auditorium', 'Classroom',
                      'Sports Field', 'Online', 'Other')
        ) if obj.purpose != 'New Semester' else 'Online'
    )

    is_hybrid = factory.LazyAttribute(
        lambda obj: True if obj.location_type != 'online' else False)
    online_link = factory.LazyAttribute(
        lambda obj: fake.url() if obj.is_hybrid else None)

    requires_registration = factory.LazyAttribute(
        lambda obj: fake.boolean() if obj.purpose != 'New Semester' else True)
    registration_start = factory.LazyAttribute(
        lambda obj: fake.past_date() if obj.requires_registration else None)
    registration_end = factory.LazyAttribute(
        lambda obj: fake.future_date() if obj.requires_registration else None)

    eligibility = factory.LazyAttribute(
        lambda obj: fake.random_element(
            elements=('All', 'Students Only', 'Faculty Only',
                      'Invitation Only')) if obj.purpose != 'New Semester' else 'All'
    )

    has_fee = factory.LazyAttribute(
        lambda obj: fake.boolean() if obj.purpose != 'New Semester' else True)
    fee_amount = factory.LazyAttribute(
        lambda obj: random.randint(100, 900) if obj.has_fee else 0.00)
    description = factory.LazyAttribute(lambda x: fake.text())

    @factory.post_generation
    def clean_data(self, create, extracted, **kwargs):
        """Post-generation hook to clean up data."""
        if not create:
            return

        return remove_fields(self)


class SemesterFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Semester
        sqlalchemy_session = None

    event = factory.SubFactory(
        EventFactory, sqlalchemy_session=Meta.sqlalchemy_session, purpose='New Semester')

    event_id = factory.LazyAttribute(lambda obj: obj.event.id)
    name = factory.LazyAttribute(lambda x: 1)

    @factory.post_generation
    def clean_data(self, create, extracted, **kwargs):
        """Post-generation hook to clean up data."""
        if not create:
            return

        return remove_fields(self, 'event')
