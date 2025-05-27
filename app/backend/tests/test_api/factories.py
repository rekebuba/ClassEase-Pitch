from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import os
from typing import Any, Generic, Optional, Type, TypeVar
from PIL import Image
import random
import bcrypt
import factory
from factory import LazyAttribute
from faker import Faker
from pyethiodate import EthDate  # type: ignore
from models.year import Year
from models.semester import Semester
from models.teacher import Teacher
from models.student import Student
from models.admin import Admin
from models.user import User
from models.event import Event
from models.base_model import CustomTypes
from sqlalchemy.orm import scoped_session, Session
from models import storage

fake = Faker()


class DefaultFelids:
    def __init__(self, session: scoped_session[Session]):
        self.session: scoped_session[Session] = session

    def set_year_id(self):
        year_id = self.session.query(Year.id).scalar()
        return year_id

    @staticmethod
    def current_EC_year() -> EthDate:
        return EthDate.date_to_ethiopian(datetime.now()).year


class BaseSQLAlchemyModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = scoped_session
        sqlalchemy_session_persistence = None

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override creation to only use provided kwargs"""
        return kwargs


class UserFactory(BaseSQLAlchemyModelFactory):
    class Meta:
        model = User

    @staticmethod
    def generate_fake_profile_picture():
        directory = "profiles"
        os.makedirs(directory, exist_ok=True)  # Ensure directory exists

        file_name = f"{directory}/{str(fake.uuid4())}.jpg"

        # Create a random image using Pillow
        image = Image.new(
            "RGB",
            (256, 256),
            (fake.random_int(0, 255), fake.random_int(0, 255), fake.random_int(0, 255)),
        )
        image.save(file_name, "JPEG")

        return file_name  # Returns the saved file path

    @staticmethod
    def _generate_id(role: CustomTypes.RoleEnum) -> str:
        """
        Generates a custom ID based on the role (Admin, Student, Teacher).

        The ID format is: <section>/<random_number>/<year_suffix>
        - Section: 'MAS' for Student, 'MAT' for Teacher, 'MAA' for Admin
        - Random number: A 4-digit number between 1000 and 9999
        - Year suffix: Last 2 digits of the current Ethiopian year
        """
        identification = ""
        section = ""

        # Assign prefix based on role
        if role == CustomTypes.RoleEnum.STUDENT:
            section = "MAS"
        elif role == CustomTypes.RoleEnum.TEACHER:
            section = "MAT"
        elif role == CustomTypes.RoleEnum.ADMIN:
            section = "MAA"

        num = random.randint(1000, 9999)
        starting_year = (
            EthDate.date_to_ethiopian(datetime.now()).year % 100
        )  # Get last 2 digits of the year
        identification = f"{section}/{num}/{starting_year}"

        return identification

    @staticmethod
    def _hash_password(password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    image_path = LazyAttribute(lambda x: UserFactory.generate_fake_profile_picture())
    national_id = LazyAttribute(lambda x: str(fake.uuid4()))
    role = LazyAttribute(lambda x: random.choice(list(CustomTypes.RoleEnum)))


class AdminFactory(BaseSQLAlchemyModelFactory):
    class Meta:
        model: Type[Admin] = Admin

    # Add additional fields for Admin
    first_name = LazyAttribute(lambda x: fake.first_name())
    father_name = LazyAttribute(lambda x: fake.last_name())
    grand_father_name = LazyAttribute(lambda x: fake.first_name())
    date_of_birth = LazyAttribute(lambda x: fake.date_of_birth())
    email = LazyAttribute(lambda x: fake.email())
    gender = LazyAttribute(lambda x: fake.random_element(elements=("M", "F")))
    phone = LazyAttribute(lambda x: "091234567")
    address = LazyAttribute(lambda x: fake.address())


class StudentFactory(BaseSQLAlchemyModelFactory):
    class Meta:
        model = Student

    # Add additional fields for Admin
    first_name = LazyAttribute(lambda x: fake.first_name())
    father_name = LazyAttribute(lambda x: fake.last_name())
    grand_father_name = LazyAttribute(lambda x: fake.first_name())
    date_of_birth = LazyAttribute(lambda x: fake.date_of_birth(minimum_age=6))
    gender = LazyAttribute(lambda x: fake.random_element(elements=("M", "F")))
    father_phone = LazyAttribute(lambda x: "091234567")
    mother_phone = LazyAttribute(lambda x: "091234567")
    guardian_name = LazyAttribute(lambda x: fake.name())
    guardian_phone = LazyAttribute(lambda x: "091234567")

    current_grade = LazyAttribute(lambda x: random.randint(1, 10))
    academic_year = LazyAttribute(lambda x: DefaultFelids.current_EC_year())

    is_transfer = LazyAttribute(lambda x: fake.boolean())
    previous_school_name = LazyAttribute(
        lambda obj: fake.company() if obj.is_transfer else ""
    )

    has_medical_condition = LazyAttribute(lambda _: fake.boolean())
    medical_details = LazyAttribute(
        lambda obj: fake.text() if obj.has_medical_condition else ""
    )
    has_disability = LazyAttribute(lambda x_: fake.boolean())
    disability_details = LazyAttribute(
        lambda obj: fake.text() if obj.has_disability else ""
    )
    requires_special_accommodation = LazyAttribute(lambda _: fake.boolean())
    special_accommodation_details = LazyAttribute(
        lambda obj: fake.text() if obj.requires_special_accommodation else ""
    )


class TeacherFactory(BaseSQLAlchemyModelFactory):
    class Meta:
        model = Teacher

    # Add additional fields for Teacher
    first_name = LazyAttribute(lambda x: fake.first_name())
    father_name = LazyAttribute(lambda x: fake.last_name())
    grand_father_name = LazyAttribute(lambda x: fake.first_name())
    date_of_birth = LazyAttribute(lambda x: fake.date_of_birth())
    email = LazyAttribute(lambda x: fake.email())
    gender = LazyAttribute(lambda x: fake.random_element(elements=("M", "F")))
    phone = LazyAttribute(lambda x: "091234567")
    address = LazyAttribute(lambda x: fake.address())
    year_of_experience = LazyAttribute(lambda x: random.randint(0, 5))
    qualification = LazyAttribute(
        lambda x: fake.random_element(
            elements=(
                "Certified Teacher",
                "Diploma in Education",
                "Degree in Education",
            )
        )
    )


class EventFactory(BaseSQLAlchemyModelFactory):
    class Meta:
        model = Event

    title = LazyAttribute(lambda x: fake.sentence())
    purpose = LazyAttribute(
        lambda x: fake.random_element(
            elements=(
                "New Semester",
                "Graduation",
                "Sports Event",
                "Administration",
                "Other",
            )
        )
    )
    organizer = LazyAttribute(
        lambda obj: fake.random_element(
            elements=(
                "School Administration",
                "School",
                "Student Club",
                "External Organizer",
            )
        )
        if obj.purpose != "New Semester"
        else "School Administration"
    )

    academic_year = LazyAttribute(lambda obj: DefaultFelids.current_EC_year())

    start_date = LazyAttribute(lambda x: fake.past_date())
    end_date = LazyAttribute(lambda x: fake.future_date())
    start_time = LazyAttribute(
        lambda x: datetime.now() - timedelta(hours=1)
    )  # Past datetime
    end_time = LazyAttribute(
        lambda x: datetime.now() + timedelta(hours=1)
    )  # Future datetime

    location = LazyAttribute(
        lambda obj: fake.random_element(
            elements=("Auditorium", "Classroom", "Sports Field", "Online", "Other")
        )
        if obj.purpose != "New Semester"
        else "Online"
    )

    is_hybrid = LazyAttribute(lambda obj: True if obj.location != "online" else False)
    online_link = LazyAttribute(lambda obj: fake.url() if obj.is_hybrid else None)

    requires_registration = LazyAttribute(
        lambda obj: fake.boolean() if obj.purpose != "New Semester" else True
    )
    registration_start = LazyAttribute(
        lambda obj: fake.past_date() if obj.requires_registration else None
    )
    registration_end = LazyAttribute(
        lambda obj: fake.future_date() if obj.requires_registration else None
    )

    eligibility = LazyAttribute(
        lambda obj: fake.random_element(
            elements=("All", "Students Only", "Faculty Only", "Invitation Only")
        )
        if obj.purpose != "New Semester"
        else "All"
    )

    has_fee = LazyAttribute(
        lambda obj: fake.boolean() if obj.purpose != "New Semester" else True
    )
    fee_amount = LazyAttribute(
        lambda obj: random.randint(100, 900) if obj.has_fee else 0.00
    )
    description = LazyAttribute(lambda x: fake.text())


class SemesterFactory(BaseSQLAlchemyModelFactory):
    class Meta:
        model = Semester

    name = LazyAttribute(lambda x: 1)


@dataclass(kw_only=True)
class AvailableSubject:
    grade: int
    subject: str
    subject_code: str


@dataclass
class AssessmentTypes:
    type: str
    percentage: int


@dataclass
class MarkAssessment:
    grade: int
    subjects: list
    assessment_type: list


@dataclass
class FakeMarkList:
    grade_num: int  # number of mark List to create based on available grades
    academic_year: int
    semester: int
    mark_assessment: dict

    def to_dict(self):
        return asdict(self)  # Converts all fields to dict automatically


class SubjectsFactory(factory.Factory):
    class Meta:
        model = AvailableSubject

    subject = LazyAttribute(lambda _: None)
    subject_code = LazyAttribute(lambda _: None)
    grade = LazyAttribute(lambda _: None)


class AssessmentTypesFactory(factory.Factory):
    class Meta:
        model = AssessmentTypes

    type = factory.Faker("random_element", elements=("Mid", "Final"))
    percentage = LazyAttribute(lambda obj: 30 if obj.type == "Mid" else 70)


class MarkAssessmentFactory(factory.Factory):
    class Meta:
        model = MarkAssessment

    grade = LazyAttribute(lambda _: random.randint(1, 10))
    subjects = LazyAttribute(lambda _: SubjectsFactory.create_batch(4))
    assessment_type = LazyAttribute(lambda _: AssessmentTypesFactory.create_batch(2))


class MarkListFactory(factory.Factory):
    class Meta:
        model = FakeMarkList

    academic_year = LazyAttribute(lambda _: DefaultFelids.current_EC_year())
    semester = LazyAttribute(lambda _: 1)
    grade_num = LazyAttribute(lambda _: 0)  # number of available grades
    mark_assessment = LazyAttribute(
        lambda obj: [MarkAssessmentFactory() for _ in range(obj.grade_num)]
    )
