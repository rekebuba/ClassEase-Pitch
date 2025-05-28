from dataclasses import dataclass, asdict
from datetime import date, datetime, timedelta
from io import BufferedReader, BytesIO
import os
from typing import Any, ClassVar, Dict, Generic, Optional, Type, TypeVar
from PIL import Image
import random
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
from werkzeug.datastructures import FileStorage
import tempfile

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
    def _create(
        cls, model_class: Any, *args: Any, **kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Override creation to only use provided kwargs"""
        for key, value in kwargs.items():
            if isinstance(value, datetime):
                if "time" in key:
                    kwargs[key] = value.strftime("%H:%M:%S")
                else:
                    kwargs[key] = value.strftime("%Y-%m-%d")
            elif isinstance(value, date):
                kwargs[key] = value.strftime("%Y-%m-%d")
        return kwargs


class UserFactory(BaseSQLAlchemyModelFactory):
    class Meta:
        model = User

    @staticmethod
    def generate_fake_profile_picture() -> BufferedReader:
        directory = "profiles"
        os.makedirs(directory, exist_ok=True)  # Ensure directory exists

        # Create a random image using Pillow
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) as tmp:
            # Generate and save image
            image = Image.new(
                "RGB",
                (256, 256),
                (
                    fake.random_int(0, 255),
                    fake.random_int(0, 255),
                    fake.random_int(0, 255),
                ),
            )
            image.save(tmp.name, format="JPEG")

            # Reopen in binary mode and return (file will auto-delete when closed)
            return open(tmp.name, "rb")

    image_path: Any = LazyAttribute(
        lambda x: UserFactory.generate_fake_profile_picture()
    )
    national_id: Any = LazyAttribute(lambda x: str(fake.uuid4()))
    role: Any = LazyAttribute(lambda x: random.choice(list(CustomTypes.RoleEnum)))


class AdminFactory(BaseSQLAlchemyModelFactory):
    class Meta:
        model = Admin

    user: Any = factory.SubFactory(UserFactory, role=CustomTypes.RoleEnum.ADMIN.value)

    # Add additional fields for Admin
    first_name: Any = LazyAttribute(lambda x: fake.first_name())
    father_name: Any = LazyAttribute(lambda x: fake.last_name())
    grand_father_name: Any = LazyAttribute(lambda x: fake.first_name())
    date_of_birth: Any = LazyAttribute(lambda x: fake.date_of_birth())
    email: Any = LazyAttribute(lambda x: fake.email())
    gender: Any = LazyAttribute(lambda x: fake.random_element(elements=("M", "F")))
    phone: Any = LazyAttribute(lambda x: "091234567")
    address: Any = LazyAttribute(lambda x: fake.address())


class StudentFactory(BaseSQLAlchemyModelFactory):
    class Meta:
        model = Student

    user: Any = factory.SubFactory(UserFactory, role=CustomTypes.RoleEnum.STUDENT.value)
    # Add additional fields for Admin
    first_name: Any = LazyAttribute(lambda x: fake.first_name())
    father_name: Any = LazyAttribute(lambda x: fake.last_name())
    grand_father_name: Any = LazyAttribute(lambda x: fake.first_name())
    date_of_birth: Any = LazyAttribute(lambda x: fake.date_of_birth(minimum_age=6))
    gender: Any = LazyAttribute(lambda x: fake.random_element(elements=("M", "F")))
    father_phone: Any = LazyAttribute(lambda x: "091234567")
    mother_phone: Any = LazyAttribute(lambda x: "091234567")
    guardian_name: Any = LazyAttribute(lambda x: fake.name())
    guardian_phone: Any = LazyAttribute(lambda x: "091234567")

    current_grade: Any = LazyAttribute(lambda x: random.randint(1, 10))
    academic_year: Any = LazyAttribute(lambda x: DefaultFelids.current_EC_year())

    is_transfer: Any = LazyAttribute(lambda x: fake.boolean())
    previous_school_name: Any = LazyAttribute(
        lambda obj: fake.company() if obj.is_transfer else ""
    )

    has_medical_condition: Any = LazyAttribute(lambda _: fake.boolean())
    medical_details: Any = LazyAttribute(
        lambda obj: fake.text() if obj.has_medical_condition else ""
    )
    has_disability: Any = LazyAttribute(lambda x_: fake.boolean())
    disability_details: Any = LazyAttribute(
        lambda obj: fake.text() if obj.has_disability else ""
    )
    requires_special_accommodation: Any = LazyAttribute(lambda _: fake.boolean())
    special_accommodation_details: Any = LazyAttribute(
        lambda obj: fake.text() if obj.requires_special_accommodation else ""
    )


class TeacherFactory(BaseSQLAlchemyModelFactory):
    class Meta:
        model = Teacher

    user: Any = factory.SubFactory(UserFactory, role=CustomTypes.RoleEnum.TEACHER.value)

    # Add additional fields for Teacher
    first_name: Any = LazyAttribute(lambda x: fake.first_name())
    father_name: Any = LazyAttribute(lambda x: fake.last_name())
    grand_father_name: Any = LazyAttribute(lambda x: fake.first_name())
    date_of_birth: Any = LazyAttribute(lambda x: fake.date_of_birth())
    email: Any = LazyAttribute(lambda x: fake.email())
    gender: Any = LazyAttribute(lambda x: fake.random_element(elements=("M", "F")))
    phone: Any = LazyAttribute(lambda x: "091234567")
    address: Any = LazyAttribute(lambda x: fake.address())
    year_of_experience: Any = LazyAttribute(lambda x: random.randint(0, 5))
    qualification: Any = LazyAttribute(
        lambda x: fake.random_element(
            elements=(
                "Certified Teacher",
                "Diploma in Education",
                "Degree in Education",
            )
        )
    )


class SemesterFactory(BaseSQLAlchemyModelFactory):
    class Meta:
        model = Semester

    name: Any = LazyAttribute(lambda x: 1)


class EventFactory(BaseSQLAlchemyModelFactory):
    class Meta:
        model = Event

    title: Any = LazyAttribute(lambda x: fake.sentence())
    purpose: Any = factory.LazyAttribute(
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

    organizer: Any = LazyAttribute(
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

    academic_year: Any = LazyAttribute(lambda obj: DefaultFelids.current_EC_year())

    start_date: Any = LazyAttribute(lambda x: fake.past_date())
    end_date: Any = LazyAttribute(lambda x: fake.future_date())
    start_time: Any = LazyAttribute(
        lambda x: datetime.now() - timedelta(hours=1)
    )  # Past datetime
    end_time: Any = LazyAttribute(
        lambda x: datetime.now() + timedelta(hours=1)
    )  # Future datetime

    location: Any = LazyAttribute(
        lambda obj: fake.random_element(
            elements=("Auditorium", "Classroom", "Sports Field", "Online", "Other")
        )
        if obj.purpose != "New Semester"
        else "Online"
    )

    is_hybrid: Any = LazyAttribute(
        lambda obj: True if obj.location != "online" else False
    )
    online_link: Any = LazyAttribute(lambda obj: fake.url() if obj.is_hybrid else None)

    requires_registration: Any = LazyAttribute(
        lambda obj: fake.boolean() if obj.purpose != "New Semester" else True
    )
    registration_start: Any = LazyAttribute(
        lambda obj: fake.past_date() if obj.requires_registration else None
    )
    registration_end: Any = LazyAttribute(
        lambda obj: fake.future_date() if obj.requires_registration else None
    )

    eligibility: Any = LazyAttribute(
        lambda obj: fake.random_element(
            elements=("All", "Students Only", "Faculty Only", "Invitation Only")
        )
        if obj.purpose != "New Semester"
        else "All"
    )

    has_fee: Any = LazyAttribute(
        lambda obj: fake.boolean() if obj.purpose != "New Semester" else True
    )
    fee_amount: Any = LazyAttribute(
        lambda obj: random.randint(100, 900) if obj.has_fee else 0.00
    )
    description: Any = LazyAttribute(lambda x: fake.text())

    @factory.post_generation
    def new_semester(obj: Dict[str, Any], create, extracted, **kwargs: Any) -> None:
        if not create:
            return

        if "purpose" in obj and obj["purpose"] == "New Semester":
            obj["semester"] = SemesterFactory()


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
    mark_assessment: Dict[str, Any]

    def to_dict(self):
        return asdict(self)  # Converts all fields to dict automatically


class SubjectsFactory(factory.Factory[Any]):
    class Meta:
        model = AvailableSubject

    subject: Any = LazyAttribute(lambda _: None)
    subject_code: Any = LazyAttribute(lambda _: None)
    grade: Any = LazyAttribute(lambda _: None)


class AssessmentTypesFactory(factory.Factory[Any]):
    class Meta:
        model = AssessmentTypes

    type = factory.Faker("random_element", elements=("Mid", "Final"))
    percentage: Any = LazyAttribute(lambda obj: 30 if obj.type == "Mid" else 70)


class MarkAssessmentFactory(factory.Factory[Any]):
    class Meta:
        model = MarkAssessment

    grade: Any = LazyAttribute(lambda _: random.randint(1, 10))
    subjects: Any = LazyAttribute(lambda _: SubjectsFactory.create_batch(4))
    assessment_type: Any = LazyAttribute(
        lambda _: AssessmentTypesFactory.create_batch(2)
    )


class MarkListFactory(factory.Factory[Any]):
    class Meta:
        model = FakeMarkList

    academic_year: Any = LazyAttribute(lambda _: DefaultFelids.current_EC_year())
    semester: Any = LazyAttribute(lambda _: 1)
    grade_num: Any = LazyAttribute(lambda _: 0)  # number of available grades
    mark_assessment: Any = LazyAttribute(
        lambda obj: [MarkAssessmentFactory() for _ in range(obj.grade_num)]
    )
