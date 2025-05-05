from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import os
from typing import Optional
from PIL import Image
import random
import bcrypt
import factory
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
from sqlalchemy.orm import scoped_session

fake = Faker()


class DefaultFelids:
    def __init__(self, session):
        self.session: Optional[scoped_session] = session

    def set_year_id(self):
        year_id = self.session.query(Year.id).scalar()
        return year_id

    @staticmethod
    def current_EC_year() -> EthDate:
        return EthDate.date_to_ethiopian(datetime.now()).year


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session: Optional[scoped_session] = None

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
    def _generate_id(role):
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

    image_path = factory.LazyAttribute(
        lambda x: UserFactory.generate_fake_profile_picture()
    )
    national_id = factory.LazyAttribute(lambda x: str(fake.uuid4()))
    role = factory.LazyAttribute(lambda x: random.choice(list(CustomTypes.RoleEnum)))
    identification = factory.LazyAttribute(
        lambda obj: UserFactory._generate_id(obj.role)
    )
    password = factory.LazyAttribute(
        lambda obj: UserFactory._hash_password(obj.identification)
    )


class AdminFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Admin
        sqlalchemy_session: Optional[scoped_session] = None

    user_id = factory.LazyAttribute(lambda _: None)  # Assign only user_id

    # Add additional fields for Admin
    first_name = factory.LazyAttribute(lambda x: fake.first_name())
    father_name = factory.LazyAttribute(lambda x: fake.last_name())
    grand_father_name = factory.LazyAttribute(lambda x: fake.first_name())
    date_of_birth = factory.LazyAttribute(lambda x: fake.date_of_birth())
    email = factory.LazyAttribute(lambda x: fake.email())
    gender = factory.LazyAttribute(lambda x: fake.random_element(elements=("M", "F")))
    phone = factory.LazyAttribute(lambda x: "091234567")
    address = factory.LazyAttribute(lambda x: fake.address())


class StudentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Student
        sqlalchemy_session: Optional[scoped_session] = None

    user_id = factory.LazyAttribute(lambda _: None)  # Assign only user_id

    # Add additional fields for Admin
    first_name = factory.LazyAttribute(lambda x: fake.first_name())
    father_name = factory.LazyAttribute(lambda x: fake.last_name())
    grand_father_name = factory.LazyAttribute(lambda x: fake.first_name())
    date_of_birth = factory.LazyAttribute(lambda x: fake.date_of_birth())
    gender = factory.LazyAttribute(lambda x: fake.random_element(elements=("M", "F")))
    father_phone = factory.LazyAttribute(lambda x: "091234567")
    mother_phone = factory.LazyAttribute(lambda x: "091234567")
    guardian_name = factory.LazyAttribute(lambda x: fake.name())
    guardian_phone = factory.LazyAttribute(lambda x: "091234567")

    start_year_id = factory.LazyAttribute(lambda x: None)
    current_year_id = factory.LazyAttribute(lambda x: None)

    is_transfer = factory.LazyAttribute(lambda x: fake.boolean())
    previous_school_name = factory.LazyAttribute(
        lambda obj: fake.company() if obj.is_transfer else ""
    )

    current_grade_id = factory.LazyAttribute(lambda x: None)
    next_grade_id = factory.LazyAttribute(lambda x: None)
    semester_id = factory.LazyAttribute(lambda x: None)
    has_passed = factory.LazyAttribute(lambda x: False)
    is_registered = factory.LazyAttribute(lambda x: False)

    has_medical_condition = factory.LazyAttribute(lambda _: fake.boolean())
    medical_details = factory.LazyAttribute(
        lambda obj: fake.text() if obj.has_medical_condition else ""
    )
    has_disability = factory.LazyAttribute(lambda x_: fake.boolean())
    disability_details = factory.LazyAttribute(
        lambda obj: fake.text() if obj.has_disability else ""
    )
    requires_special_accommodation = factory.LazyAttribute(lambda _: fake.boolean())
    special_accommodation_details = factory.LazyAttribute(
        lambda obj: fake.text() if obj.requires_special_accommodation else ""
    )

    is_active = factory.LazyAttribute(lambda x: True)


class TeacherFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Teacher
        sqlalchemy_session: Optional[scoped_session] = None

    user_id = factory.LazyAttribute(lambda _: None)  # Assign only user_id
    # Add additional fields for Teacher
    first_name = factory.LazyAttribute(lambda x: fake.first_name())
    father_name = factory.LazyAttribute(lambda x: fake.last_name())
    grand_father_name = factory.LazyAttribute(lambda x: fake.first_name())
    date_of_birth = factory.LazyAttribute(lambda x: fake.date_of_birth())
    email = factory.LazyAttribute(lambda x: fake.email())
    gender = factory.LazyAttribute(lambda x: fake.random_element(elements=("M", "F")))
    phone = factory.LazyAttribute(lambda x: "091234567")
    address = factory.LazyAttribute(lambda x: fake.address())
    year_of_experience = factory.LazyAttribute(lambda x: random.randint(0, 5))
    qualification = factory.LazyAttribute(
        lambda x: fake.random_element(
            elements=(
                "Certified Teacher",
                "Diploma in Education",
                "Degree in Education",
            )
        )
    )


class EventFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Event
        sqlalchemy_session: Optional[scoped_session] = None

    title = factory.LazyAttribute(lambda x: fake.sentence())
    purpose = factory.LazyAttribute(
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
    organizer = factory.LazyAttribute(
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

    year_id = factory.LazyAttribute(lambda x: None)

    start_date = factory.LazyAttribute(lambda x: fake.past_date())
    end_date = factory.LazyAttribute(lambda x: fake.future_date())
    start_time = factory.LazyAttribute(
        lambda x: datetime.now() - timedelta(hours=1)
    )  # Past datetime
    end_time = factory.LazyAttribute(
        lambda x: datetime.now() + timedelta(hours=1)
    )  # Future datetime

    location = factory.LazyAttribute(
        lambda obj: fake.random_element(
            elements=("Auditorium", "Classroom", "Sports Field", "Online", "Other")
        )
        if obj.purpose != "New Semester"
        else "Online"
    )

    is_hybrid = factory.LazyAttribute(
        lambda obj: True if obj.location != "online" else False
    )
    online_link = factory.LazyAttribute(
        lambda obj: fake.url() if obj.is_hybrid else None
    )

    requires_registration = factory.LazyAttribute(
        lambda obj: fake.boolean() if obj.purpose != "New Semester" else True
    )
    registration_start = factory.LazyAttribute(
        lambda obj: fake.past_date() if obj.requires_registration else None
    )
    registration_end = factory.LazyAttribute(
        lambda obj: fake.future_date() if obj.requires_registration else None
    )

    eligibility = factory.LazyAttribute(
        lambda obj: fake.random_element(
            elements=("All", "Students Only", "Faculty Only", "Invitation Only")
        )
        if obj.purpose != "New Semester"
        else "All"
    )

    has_fee = factory.LazyAttribute(
        lambda obj: fake.boolean() if obj.purpose != "New Semester" else True
    )
    fee_amount = factory.LazyAttribute(
        lambda obj: random.randint(100, 900) if obj.has_fee else 0.00
    )
    description = factory.LazyAttribute(lambda x: fake.text())


class SemesterFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Semester
        sqlalchemy_session: Optional[scoped_session] = None

    event_id = factory.LazyAttribute(lambda _: None)
    name = factory.LazyAttribute(lambda x: 1)


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

    subject = factory.LazyAttribute(lambda _: None)
    subject_code = factory.LazyAttribute(lambda _: None)
    grade = factory.LazyAttribute(lambda _: None)


class AssessmentTypesFactory(factory.Factory):
    class Meta:
        model = AssessmentTypes

    type = factory.Faker("random_element", elements=("Mid", "Final"))
    percentage = factory.LazyAttribute(lambda obj: 30 if obj.type == "Mid" else 70)


class MarkAssessmentFactory(factory.Factory):
    class Meta:
        model = MarkAssessment

    grade = factory.LazyAttribute(lambda _: random.randint(1, 10))
    subjects = factory.LazyAttribute(lambda _: SubjectsFactory.create_batch(4))
    assessment_type = factory.LazyAttribute(
        lambda _: AssessmentTypesFactory.create_batch(2)
    )


class MarkListFactory(factory.Factory):
    class Meta:
        model = FakeMarkList

    academic_year = factory.LazyAttribute(lambda _: DefaultFelids.current_EC_year())
    semester = factory.LazyAttribute(lambda _: 1)
    grade_num = factory.LazyAttribute(lambda _: 0)  # number of available grades
    mark_assessment = factory.LazyAttribute(
        lambda obj: [MarkAssessmentFactory() for _ in range(obj.grade_num)]
    )
