import random
import factory
from faker import Faker

from models.student import Student
from models.admin import Admin
from models.user import User

fake = Faker()


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = None

    national_id = factory.LazyAttribute(lambda x: str(fake.uuid4()))


class AdminFactory(UserFactory):
    class Meta:
        model = Admin
        sqlalchemy_session = None

    # Add additional fields for Admin
    first_name = factory.LazyAttribute(lambda x: fake.first_name())
    father_name = factory.LazyAttribute(lambda x: fake.last_name())
    grand_father_name = factory.LazyAttribute(lambda x: fake.first_name())
    date_of_birth = factory.LazyAttribute(
        lambda x: str(fake.date_of_birth().strftime('%Y-%m-%d'))
    )
    email = factory.LazyAttribute(lambda x: fake.email())
    gender = factory.LazyAttribute(
        lambda x: fake.random_element(elements=('M', 'F')))
    phone = factory.LazyAttribute(lambda x: '091234567')
    address = factory.LazyAttribute(lambda x: fake.address())


class StudentFactory(UserFactory):
    class Meta:
        model = Student
        sqlalchemy_session = None

    # Add additional fields for Admin
    first_name = factory.LazyAttribute(lambda x: fake.first_name())
    father_name = factory.LazyAttribute(lambda x: fake.last_name())
    grand_father_name = factory.LazyAttribute(lambda x: fake.first_name())
    date_of_birth = factory.LazyAttribute(
        lambda x: str(fake.date_of_birth().strftime('%Y-%m-%d'))
    )
    gender = factory.LazyAttribute(
        lambda x: fake.random_element(elements=('M', 'F')))
    father_phone = factory.LazyAttribute(lambda x: '091234567')
    mother_phone = factory.LazyAttribute(lambda x: '091234567')
    guardian_name = factory.LazyAttribute(lambda x: fake.name())
    guardian_phone = factory.LazyAttribute(lambda x: '091234567')

    is_transfer = factory.LazyAttribute(lambda x: fake.boolean())
    previous_school_name = factory.Maybe(
        'is_transfer',
        factory.LazyAttribute(lambda x: fake.company()),
        None
    )

    current_grade = factory.LazyAttribute(lambda x: random.randint(1, 12))
    semester_id = factory.LazyAttribute(lambda x: str(fake.uuid4()))
    has_passed = factory.LazyAttribute(lambda x: False)

    has_medical_condition = factory.LazyAttribute(lambda _: fake.boolean())
    medical_details = factory.Maybe(
        'has_medical_condition',
        factory.LazyAttribute(lambda _: fake.text()),
        None
    )
    has_disability = factory.LazyAttribute(lambda _: fake.boolean())
    disability_details = factory.Maybe(
        'has_disability',
        factory.LazyAttribute(lambda _: fake.text()),
        None
    )
    requires_special_accommodation = factory.LazyAttribute(
        lambda _: fake.boolean())
    special_accommodation_details = factory.Maybe(
        'requires_special_accommodation',
        factory.LazyAttribute(lambda _: fake.text()),
        None
    )

    is_active = factory.LazyAttribute(lambda x: fake.boolean())
