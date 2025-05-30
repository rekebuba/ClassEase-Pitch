from typing import (
    Any,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
)
import os
import random
import factory
import bcrypt
from PIL import Image
from dataclasses import dataclass, asdict
from datetime import date, datetime, timedelta
from io import BufferedReader
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
from models.grade import Grade
from factory.alchemy import SQLAlchemyModelFactory
from models import storage
from factory.fuzzy import FuzzyChoice
from models.base_model import CustomTypes
from sqlalchemy.orm import scoped_session, Session
import tempfile

fake = Faker()
T = TypeVar("T")


class DefaultFelids:
    def __init__(self, session: scoped_session[Session]):
        self.session: scoped_session[Session] = session

    def set_year_id(self):
        year_id = self.session.query(Year.id).scalar()
        return year_id

    @staticmethod
    def current_EC_year() -> EthDate:
        return EthDate.date_to_ethiopian(datetime.now()).year


class BaseFactory(SQLAlchemyModelFactory, Generic[T]):  # type: ignore[type-arg]
    """Base factory class for creating database models."""

    class Meta:
        abstract = True
        sqlalchemy_session = storage.session
        sqlalchemy_session_persistence = None

    @classmethod
    def get_or_create(cls: Type["BaseFactory[T]"], **kwargs: Any) -> T:
        model = getattr(cls._meta, "model", None)
        session = getattr(cls._meta, "sqlalchemy_session", None)
        if model is None or session is None:
            raise ValueError(
                "Model and session must be defined in the factory's Meta class."
            )

        # Use Meta.get_or_create_fields if specified
        lookup_fields = getattr(cls._meta, "get_or_create_fields", None)
        lookup_kwargs = {
            k: v
            for k, v in kwargs.items()
            if lookup_fields is None or k in lookup_fields
        }

        existing = session.query(model).filter_by(**lookup_kwargs).first()
        if existing:
            return existing  # type: ignore[no-any-return]

        return cls.create(**kwargs)

    @classmethod
    def _create(
        cls: Type["BaseFactory[T]"], model_class: Type[T], *arg: Any, **kwargs: Any
    ) -> T:
        """
        Override creation to skip specific fields marked in _skip_for_session
        """
        add_fields = getattr(cls, "_add_for_session", {})

        # Add to attributes
        for field, value in add_fields.items():
            all_args = field.split(".")
            key = all_args[0]
            args = {}
            for v in all_args[1:]:
                args[v] = kwargs.get(v, None)
            kwargs[key] = value(**args)

        return super()._create(model_class, *arg, **kwargs)  # type: ignore[no-any-return]

    @classmethod
    def _build(
        cls: Type["BaseFactory[T]"], model_class: Type[T], *arg: Any, **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Override creation to skip specific fields marked in _skip_for_session
        """
        add_fields = getattr(cls, "_add_for_test", {})

        # Add to attributes
        for field, value in add_fields.items():
            all_args = field.split(".")
            key = all_args[0]
            args = {}
            for v in all_args[1:]:
                args[v] = kwargs.get(v, None)
            kwargs[key] = value(**args)

        for key, value in kwargs.items():
            if isinstance(value, datetime):
                if "time" in key:
                    kwargs[key] = value.strftime("%H:%M:%S")
                else:
                    kwargs[key] = value.strftime("%Y-%m-%d")
            elif isinstance(value, date):
                kwargs[key] = value.strftime("%Y-%m-%d")

        return kwargs

    @classmethod
    def create(cls: Type["BaseFactory[T]"], **kwargs: Any) -> T:
        return super().create(**kwargs)  # type: ignore[no-any-return]


class YearModelFactory(BaseFactory[Year]):
    """Factory for creating Year instances in the database."""

    class Meta:
        model = Year

    # Preload existing school IDs
    _existing_ids = storage.session.query(Year.id).scalar()

    @classmethod
    def get_existing_id(cls) -> Optional[str]:
        return cls._existing_ids if cls._existing_ids else None


class GradeModelFactory(BaseFactory[Grade]):
    class Meta:
        model: Grade

    # preload IDs
    _existing_ids = storage.session.query(Grade.grade, Grade.id).all()

    @classmethod
    def get_existing_id(cls, grade: int) -> Optional[str]:
        """
        Returns an existing grade ID if available, otherwise None.
        """
        for existing_grade, existing_id in cls._existing_ids:
            if existing_grade == grade:
                return str(existing_id) if existing_id is not None else None
        # If no matching grade found, return None
        return None


class EventFactory(BaseFactory[Event]):
    class Meta:
        model = Event

    _add_for_session: Dict[str, Any] = {
        "year_id": lambda **kwarg: YearModelFactory.get_existing_id(),
    }
    _add_for_test: Dict[str, Any] = {
        "academic_year": lambda **kwarg: EthDate.date_to_ethiopian(datetime.now()).year,
        "semester": lambda **kwarg: SemesterFactory.build(),
    }

    title: Any = LazyAttribute(lambda x: fake.sentence())
    purpose: Any = FuzzyChoice(
        [
            "Academic",
            "Cultural",
            "Sports",
            "Graduation",
            "Administration",
            "New Semester",
            "Other",
        ]
    )

    organizer: Any = LazyAttribute(
        lambda obj: FuzzyChoice(
            ["School Administration", "School", "Student Club", "External Organizer"]
        )
        if obj.purpose != "New Semester"
        else "School Administration"
    )

    start_date: Any = LazyAttribute(lambda x: fake.past_date())
    end_date: Any = LazyAttribute(lambda x: fake.future_date())
    start_time: Any = LazyAttribute(
        lambda x: datetime.now() - timedelta(hours=1)
    )  # Past datetime
    end_time: Any = LazyAttribute(
        lambda x: datetime.now() + timedelta(hours=1)
    )  # Future datetime

    location: Any = LazyAttribute(
        lambda obj: FuzzyChoice(
            ["Auditorium", "Classroom", "Sports Field", "Online", "Other"]
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
        lambda obj: FuzzyChoice(
            ["All", "Students Only", "Faculty Only", "Invitation Only"]
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


class SemesterFactory(BaseFactory[Semester]):
    """Factory for creating Semester instances."""

    class Meta:
        model = Semester

    _add_for_session: Dict[str, Any] = {
        "event_id": lambda **kwarg: EventFactory.get_or_create(
            purpose="New Semester", requires_registration=True, is_hybrid=False
        ).id,
    }
    _add_for_test: Dict[str, Any] = {}

    name: int = 1


class UserFactory(BaseFactory[User]):
    class Meta:
        model = User
        sqlalchemy_session = storage.session

    _add_for_test: Dict[str, Any] = {}
    _add_for_session: Dict[str, Any] = {
        "identification.role": lambda **kwarg: UserFactory._generate_id(kwarg["role"]),
        "password.identification": lambda **kwarg: UserFactory._hash_password(
            kwarg["identification"]
        ),
    }

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
        else:
            raise ValueError(f"Invalid role: {role}")

        num = random.randint(1000, 9999)
        starting_year = (
            EthDate.date_to_ethiopian(datetime.now()).year % 100
        )  # Get last 2 digits of the year
        identification = f"{section}/{num}/{starting_year}"

        return identification

    @staticmethod
    def _hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    image_path: Any = LazyAttribute(
        lambda x: UserFactory.generate_fake_profile_picture()
    )
    national_id: Any = LazyAttribute(lambda x: str(fake.uuid4()))
    role: Any = LazyAttribute(lambda x: random.choice(list(CustomTypes.RoleEnum)))


class AdminFactory(BaseFactory[Admin]):
    class Meta:
        model = Admin
        sqlalchemy_session = storage.session

    _add_for_session: Dict[str, Any] = {
        "user_id": lambda **kwarg: UserFactory.create(
            role=CustomTypes.RoleEnum.ADMIN
        ).id,
    }
    _add_for_test: Dict[str, Any] = {
        "user": lambda **kwarg: UserFactory.build(
            role=CustomTypes.RoleEnum.ADMIN.value
        ),
    }

    # Add additional fields for Admin
    first_name: Any = LazyAttribute(lambda x: fake.first_name())
    father_name: Any = LazyAttribute(lambda x: fake.last_name())
    grand_father_name: Any = LazyAttribute(lambda x: fake.first_name())
    date_of_birth: Any = LazyAttribute(lambda x: fake.date_of_birth())
    email: Any = LazyAttribute(lambda x: fake.email())
    gender: Any = LazyAttribute(lambda x: fake.random_element(elements=("M", "F")))
    phone: Any = LazyAttribute(lambda x: "091234567")
    address: Any = LazyAttribute(lambda x: fake.address())


class StudentFactory(BaseFactory[Student]):
    class Meta:
        model = Student
        sqlalchemy_session = storage.session

    _add_for_session: Dict[str, Any] = {
        "user_id": lambda **kwarg: UserFactory.create(
            role=CustomTypes.RoleEnum.STUDENT
        ).id,
        "start_year_id": lambda **kwarg: YearModelFactory.get_existing_id(),
        "current_year_id": lambda **kwarg: YearModelFactory.get_existing_id(),
        "current_grade_id": lambda **kwarg: GradeModelFactory.get_existing_id(
            random.randint(1, 12)
        ),
        "next_grade_id": lambda **kwarg: None,
        "semester_id": lambda **kwarg: SemesterFactory.get_or_create(
            event_id=EventFactory.get_or_create(
                purpose="New Semester", requires_registration=True, is_hybrid=False
            ).id
        ).id,
    }
    _add_for_test: Dict[str, Any] = {
        "user": lambda **kwarg: UserFactory.build(
            role=CustomTypes.RoleEnum.STUDENT.value
        ),
        "current_grade": lambda **kwarg: random.randint(1, 10),
        "academic_year": lambda **kwarg: EthDate.date_to_ethiopian(datetime.now()).year,
    }

    # Add additional fields for Admin
    first_name: Any = LazyAttribute(lambda x: fake.first_name())
    father_name: Any = LazyAttribute(lambda x: fake.last_name())
    grand_father_name: Any = LazyAttribute(lambda x: fake.first_name())
    date_of_birth: Any = LazyAttribute(lambda x: fake.date_of_birth(minimum_age=6))
    gender: Any = LazyAttribute(lambda x: fake.random_element(elements=("M", "F")))

    # Parent/Guardian Contacts
    father_phone: Any = LazyAttribute(lambda x: "091234567")
    mother_phone: Any = LazyAttribute(lambda x: "091234567")
    guardian_name: Any = LazyAttribute(lambda x: fake.name())
    guardian_phone: Any = LazyAttribute(lambda x: "091234567")

    has_passed: Any = LazyAttribute(lambda _: False)
    is_registered: Any = LazyAttribute(lambda _: False)

    is_transfer: Any = LazyAttribute(lambda x: fake.boolean())
    previous_school_name: Any = LazyAttribute(
        lambda obj: fake.company() if obj.is_transfer else None
    )

    # Health & Special Needs
    has_medical_condition: Any = LazyAttribute(lambda _: fake.boolean())
    medical_details: Any = LazyAttribute(
        lambda obj: fake.text(max_nb_chars=60) if obj.has_medical_condition else None
    )
    has_disability: Any = LazyAttribute(lambda x_: fake.boolean())
    disability_details: Any = LazyAttribute(
        lambda obj: fake.text(max_nb_chars=60) if obj.has_disability else None
    )
    requires_special_accommodation: Any = LazyAttribute(lambda _: fake.boolean())
    special_accommodation_details: Any = LazyAttribute(
        lambda obj: fake.text() if obj.requires_special_accommodation else None
    )


class TeacherFactory(BaseFactory[Teacher]):
    class Meta:
        model = Teacher
        sqlalchemy_session = storage.session

    _add_for_session: Dict[str, Any] = {
        "user_id": lambda **kwarg: UserFactory.create(
            role=CustomTypes.RoleEnum.TEACHER
        ).id,
    }
    _add_for_test: Dict[str, Any] = {
        "user": lambda **kwarg: UserFactory.build(
            role=CustomTypes.RoleEnum.TEACHER.value
        ),
    }

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
