from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Sequence,
    Type,
    TypeVar,
)
import os
import random
import factory
import bcrypt
from PIL import Image
from dataclasses import dataclass, asdict, field
from datetime import date, datetime, timedelta
from io import BufferedReader
from factory import LazyAttribute, SubFactory
from faker import Faker
from pyethiodate import EthDate  # type: ignore
from sqlalchemy import select
from sqlmodel import col
from models.assessment import Assessment
from models.section import Section
from models.stud_semester_record import STUDSemesterRecord
from models.stud_year_record import STUDYearRecord
from models.subject import Subject
from models.subject_grade_stream_link import SubjectGradeStreamLink
from models.table import Table
from models.teacher_grade_link import TeacherGradeLink
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

    def set_year_id(self) -> str | None:
        year_id = self.session.execute(select(Year.id)).scalar_one_or_none()
        return year_id

    @staticmethod
    def current_EC_year() -> EthDate:
        return EthDate.date_to_ethiopian(datetime.now()).year


class BaseFactory(SQLAlchemyModelFactory, Generic[T]):  # type: ignore[type-arg]
    """Base factory class for creating database models."""

    class Meta:
        abstract = True
        sqlalchemy_session = storage.session
        sqlalchemy_session_persistence = "commit"

    @classmethod
    def get_or_create(cls: Type["BaseFactory[T]"], **kwargs: Any) -> T:
        model = getattr(cls._meta, "model", None)
        session: Optional[scoped_session[Session]] = getattr(
            cls._meta, "sqlalchemy_session", None
        )
        if model is None or session is None:
            raise ValueError(
                "Model and session must be defined in the factory's Meta class."
            )

        lookup_kwargs = {k: v for k, v in kwargs.items()}

        existing = session.query(model).filter_by(**lookup_kwargs).first()
        if existing:
            return existing  # type: ignore[no-any-return]

        return cls.create(**kwargs)

    @classmethod
    def get(
        cls: Type["BaseFactory[T]"], **kwargs: Any
    ) -> Optional[scoped_session[Session]]:
        model = getattr(cls._meta, "model", None)
        session: Optional[Session] = getattr(cls._meta, "sqlalchemy_session", None)
        if model is None or session is None:
            raise ValueError(
                "Model and session must be defined in the factory's Meta class."
            )

        lookup_kwargs = {k: v for k, v in kwargs.items()}

        existing = session.query(model).filter_by(**lookup_kwargs).first()
        if existing:
            return existing  # type: ignore[no-any-return]

        return None

    @classmethod
    def _create(
        cls: Type["BaseFactory[T]"], model_class: Type[T], *arg: Any, **kwargs: Any
    ) -> T:
        """
        Override creation to add specific fields marked in _add_for_session
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

        # Skip fields that are not needed for the session
        skip_fields = getattr(cls, "_skip_fields", [])
        for k in skip_fields:
            kwargs.pop(k, None)

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

        # Skip fields that are not needed for the test
        skip_fields = getattr(cls, "_skip_fields", [])
        for field in skip_fields:
            kwargs.pop(field, None)

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


class TypedFactory(factory.Factory, Generic[T]):  # type: ignore[type-arg]
    class Meta:
        model = None  # Placeholder, set in subclasses

    @classmethod
    def build(cls, **kwargs: Any) -> T:
        return super().build(**kwargs)  # type: ignore[no-any-return]

    @classmethod
    def create(cls, **kwargs: Any) -> T:
        return super().create(**kwargs)  # type: ignore[no-any-return]


class YearModelFactory(BaseFactory[Year]):
    """Factory for creating Year instances in the database."""

    class Meta:
        model = Year

    # Preload existing school IDs
    _existing_ids = storage.session.execute(select(Year.id)).scalar_one_or_none()

    @classmethod
    def get_existing_id(cls) -> Optional[str]:
        return cls._existing_ids if cls._existing_ids else None


class GradeModelFactory(BaseFactory[Grade]):
    class Meta:
        model: Grade

    # preload IDs
    _existing_ids = storage.session.execute(select(Grade.grade, Grade.id)).all()

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
    # _add_for_test: Dict[str, Any] = {}

    name: int = 1

    def __init__(self, *args, **kwargs):
        name = kwargs.get("name", self.name)
        if name not in [1, 2]:
            raise ValueError(f"Invalid semester name: {name}. Only 1 or 2 are allowed.")

        # check if semester 1 was created before creating semester 2
        if name == 2:
            semester_1 = SemesterFactory.get(name=1)
            if semester_1 is None:
                raise ValueError("Semester 1 must be created before Semester 2.")

        # Call the parent constructor
        super().__init__(*args, **kwargs)


class UserFactory(BaseFactory[User]):
    class Meta:
        model = User
        sqlalchemy_session = storage.session

    _add_for_test: Dict[str, Any] = {}
    _add_for_session: Dict[str, Any] = {
        "identification.role.count": lambda **kwarg: UserFactory._generate_id(
            kwarg["role"], kwarg["count"]
        ),
        "password.identification": lambda **kwarg: UserFactory._hash_password(
            kwarg["identification"]
        ),
    }
    _skip_fields: List[str] = ["count"]

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
    def _generate_id(role: "CustomTypes.RoleEnum", count: int) -> str:
        """
        Generates a custom ID based on the role (Admin, Student, Teacher).

        The ID format is: <section>/<random_number>/<year_suffix>
        - Section: 'MAS' for Student, 'MAT' for Teacher, 'MAA' for Admin
        - Random number: A 4-digit number between 1000 and 9999
        - Year suffix: Last 2 digits of the current Ethiopian year
        """
        identification: str = ""
        section: str = ""

        # Assign prefix based on role
        if role == CustomTypes.RoleEnum.STUDENT:
            section = "MAS"
        elif role == CustomTypes.RoleEnum.TEACHER:
            section = "MAT"
        elif role == CustomTypes.RoleEnum.ADMIN:
            section = "MAA"
        else:
            raise ValueError(f"Invalid role: {role}")

        starting_year: int = (
            EthDate.date_to_ethiopian(datetime.now()).year % 100
        )  # Get last 2 digits of the year
        identification = f"{section}/{count}/{starting_year}"

        return identification

    @staticmethod
    def _hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    count: Any = LazyAttribute(
        lambda x: fake.random_int()
    )  # Unique identifier for each user, starting at 1000

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
        "current_grade_id.grade_id": lambda **kwarg: kwarg.get("grade_id"),
        "next_grade_id": lambda **kwarg: None,
        "semester_id": lambda **kwarg: None,
    }
    _add_for_test: Dict[str, Any] = {
        "user": lambda **kwarg: UserFactory.build(
            role=CustomTypes.RoleEnum.STUDENT.value
        ),
        "current_grade": lambda **kwarg: random.randint(1, 10),
        "academic_year": lambda **kwarg: EthDate.date_to_ethiopian(datetime.now()).year,
    }
    _skip_fields: List[str] = ["grade_id"]

    grade_id: Any = LazyAttribute(
        lambda _: GradeModelFactory.get_existing_id(random.randint(1, 12))
    )

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
        exclude = ("for_session", "grades_model", "subjects_model")

    @staticmethod
    def subject_model(grades: Sequence[Grade]) -> Sequence[Subject]:
        subject_ids = storage.session.scalars(
            select(SubjectGradeStreamLink.subject_id)
            .where(
                col(SubjectGradeStreamLink.grade_id).in_([grade.id for grade in grades])
            )
            .distinct()
        ).all()

        subjects = storage.session.scalars(
            select(Subject).where(
                col(Subject.id).in_(
                    random.choices(
                        subject_ids, k=random.choice(range(len(subject_ids)))
                    ),
                )
            )
        ).all()

        return subjects

    user: Any = SubFactory(UserFactory, role=CustomTypes.RoleEnum.TEACHER)

    for_session: Any = False
    grades_model: Any = LazyAttribute(
        lambda x: storage.session.scalars(
            select(Grade).where(
                col(Grade.level).in_(
                    random.choices(
                        list(CustomTypes.GradeLevelEnum._value2member_map_), k=2
                    )
                )
            )
        ).all()
    )
    subjects_model: Any = LazyAttribute(
        lambda x: TeacherFactory.subject_model(x.grades_model)
    )

    # Add additional fields for Teacher
    first_name: Any = LazyAttribute(lambda x: fake.first_name())
    father_name: Any = LazyAttribute(lambda x: fake.last_name())
    grand_father_name: Any = LazyAttribute(lambda x: fake.first_name())
    preferred_name: Any = LazyAttribute(
        lambda x: fake.first_name() if random.choice([True, False]) else None
    )
    date_of_birth: Any = LazyAttribute(lambda x: fake.date_of_birth())
    gender: Any = LazyAttribute(
        lambda x: random.choice(list(CustomTypes.GenderEnum._value2member_map_))
    )
    nationality: Any = LazyAttribute(lambda x: fake.country())
    marital_status: Any = LazyAttribute(
        lambda x: random.choice(list(CustomTypes.MaritalStatusEnum._value2member_map_))
    )
    social_security_number: Any = LazyAttribute(lambda x: str(fake.uuid4()))
    # Contact Information
    address: Any = LazyAttribute(lambda x: fake.address())
    city: Any = LazyAttribute(lambda x: fake.city())
    state: Any = LazyAttribute(lambda x: fake.state())
    postal_code: Any = LazyAttribute(lambda x: fake.postcode())
    country: Any = LazyAttribute(lambda x: fake.country())
    primary_phone: Any = LazyAttribute(lambda x: fake.basic_phone_number())
    secondary_phone: Any = LazyAttribute(lambda x: fake.basic_phone_number())
    personal_email: Any = LazyAttribute(lambda x: fake.email())
    work_email: Any = LazyAttribute(lambda x: fake.email())

    # Emergency Contact
    emergency_contact_name: Any = LazyAttribute(lambda x: fake.name())
    emergency_contact_relationship: Any = LazyAttribute(
        lambda x: fake.random_element(
            elements=("Parent", "Sibling", "Spouse", "Friend", "Other")
        )
    )
    emergency_contact_phone: Any = LazyAttribute(lambda x: fake.phone_number())
    emergency_contact_email: Any = LazyAttribute(lambda x: fake.email())

    # Educational Background
    highest_degree: Any = LazyAttribute(
        lambda x: fake.random_element(
            elements=(
                "High School Diploma",
                "Bachelor's Degree",
                "Master's Degree",
                "PhD",
                "Other",
            )
        )
    )
    major_subject: Any = LazyAttribute(
        lambda x: fake.random_element(
            elements=(
                "Mathematics",
                "Science",
                "English",
                "History",
                "Physical Education",
                "Art",
                "Music",
                "Other",
            )
        )
    )
    minor_subject: Any = LazyAttribute(
        lambda x: fake.random_element(
            elements=(
                "Mathematics",
                "Science",
                "English",
                "History",
                "Physical Education",
                "Art",
                "Music",
                "Other",
            )
        )
    )
    university: Any = LazyAttribute(lambda x: fake.company())
    graduation_year: Any = LazyAttribute(lambda x: random.randint(2000, 2023))
    gpa: Any = LazyAttribute(lambda x: round(random.uniform(1.0, 4.0), 2))
    additional_degrees: Any = LazyAttribute(
        lambda x: fake.text(max_nb_chars=60) if random.choice([True, False]) else None
    )

    # Teaching Certifications & Licenses
    teaching_license: Any = LazyAttribute(lambda x: fake.boolean())
    license_number: Any = LazyAttribute(
        lambda x: str(fake.uuid4()) if x.teaching_license else None
    )
    license_state: Any = LazyAttribute(
        lambda x: fake.state() if x.teaching_license else None
    )
    license_expiration_date: Any = LazyAttribute(
        lambda x: fake.future_date() if x.teaching_license else None
    )
    certifications: Any = LazyAttribute(
        lambda x: fake.text(max_nb_chars=60) if random.choice([True, False]) else None
    )
    specializations: Any = LazyAttribute(
        lambda x: fake.text(max_nb_chars=60) if random.choice([True, False]) else None
    )

    # Teaching Experience
    years_of_experience: Any = LazyAttribute(
        lambda x: random.choice(list(CustomTypes.ExperienceYearEnum._value2member_map_))
    )
    previous_schools: Any = LazyAttribute(
        lambda x: fake.text(max_nb_chars=60) if random.choice([True, False]) else None
    )

    grade_level: Any = LazyAttribute(
        lambda x: x.grades_model
        if x.for_session
        else list(set([grade.level.value for grade in x.grades_model]))
    )
    subjects_to_teach: Any = LazyAttribute(
        lambda x: x.subjects_model
        if x.for_session
        else [subject.name for subject in x.subjects_model]
    )
    preferred_schedule: Any = LazyAttribute(
        lambda x: fake.random_element(list(CustomTypes.ScheduleEnum._value2member_map_))
    )

    # Professional Skills & Qualifications
    languages_spoken: Any = LazyAttribute(
        lambda x: random.choice(["English", "Amharic", "French", "Japanese", "Chinese"])
    )
    technology_skills: Any = LazyAttribute(
        lambda x: random.choice(
            [
                "Microsoft Office Suite",
                "Google Workspace",
                "Learning Management Systems (LMS)",
                "Educational Technology Tools",
                "Coding and Programming",
                "Data Analysis Tools",
            ]
        )
    )
    special_skills: Any = LazyAttribute(
        lambda x: fake.text(max_nb_chars=30) if random.choice([True, False]) else None
    )
    professional_development: Any = LazyAttribute(
        lambda x: fake.text(max_nb_chars=60) if random.choice([True, False]) else None
    )

    # Employment Information
    position_applying_for: Any = LazyAttribute(
        lambda x: fake.random_element(
            elements=(
                "Math Teacher",
                "Science Teacher",
                "English Teacher",
                "History Teacher",
                "Physical Education Teacher",
                "Art Teacher",
                "Music Teacher",
                "Special Education Teacher",
            )
        )
    )

    # Background & References
    has_convictions: Any = LazyAttribute(lambda _: fake.boolean())
    conviction_details: Any = LazyAttribute(
        lambda obj: fake.text(max_nb_chars=60) if obj.has_convictions else None
    )
    has_disciplinary_actions: Any = LazyAttribute(lambda _: fake.boolean())
    disciplinary_details: Any = LazyAttribute(
        lambda obj: fake.text(max_nb_chars=60) if obj.has_disciplinary_actions else None
    )
    reference1_name: Any = LazyAttribute(lambda x: fake.name())
    reference1_title: Any = LazyAttribute(lambda x: fake.job())
    reference1_organization: Any = LazyAttribute(lambda x: fake.company())
    reference1_phone: Any = LazyAttribute(lambda x: fake.phone_number())
    reference1_email: Any = LazyAttribute(lambda x: fake.email())
    reference2_name: Any = LazyAttribute(lambda x: fake.name())
    reference2_title: Any = LazyAttribute(lambda x: fake.job())
    reference2_organization: Any = LazyAttribute(lambda x: fake.company())
    reference2_phone: Any = LazyAttribute(lambda x: fake.phone_number())
    reference2_email: Any = LazyAttribute(lambda x: fake.email())
    reference3_name: Any = LazyAttribute(lambda x: fake.name())
    reference3_title: Any = LazyAttribute(lambda x: fake.job())
    reference3_organization: Any = LazyAttribute(lambda x: fake.company())
    reference3_phone: Any = LazyAttribute(lambda x: fake.phone_number())
    reference3_email: Any = LazyAttribute(lambda x: fake.email())

    # Documents
    resume: Any = LazyAttribute(lambda x: fake.file_name(extension="pdf"))
    cover_letter: Any = LazyAttribute(lambda x: fake.file_name(extension="pdf"))
    transcripts: Any = LazyAttribute(lambda x: fake.file_name(extension="pdf"))
    teaching_certificate: Any = LazyAttribute(lambda x: fake.file_name(extension="pdf"))
    background_check: Any = LazyAttribute(lambda x: fake.file_name(extension="pdf"))

    # Additional Information
    teaching_philosophy: Any = LazyAttribute(
        lambda x: fake.text(max_nb_chars=1000) if random.choice([True, False]) else None
    )
    why_teaching: Any = LazyAttribute(
        lambda x: fake.text(max_nb_chars=500) if random.choice([True, False]) else None
    )
    additional_comments: Any = LazyAttribute(
        lambda x: fake.text(max_nb_chars=500) if random.choice([True, False]) else None
    )
    agree_to_terms: Any = LazyAttribute(lambda _: True)
    agree_to_background_check: Any = LazyAttribute(lambda _: True)


class SubjectFactory(BaseFactory[Subject]):
    class Meta:
        model = Subject

    @classmethod
    def get_existing_id(cls, student_grade_id: str, offset: int) -> str:
        """
        Returns an existing subject ID if available, otherwise raise ValueError.
        """
        stmt = (
            select(Subject.id)
            .join(Grade)
            .where(Grade.id == student_grade_id)
            .order_by(Subject.id)
            .offset(offset)
            .limit(1)
        )

        result = storage.session.scalars(stmt).first()  # returns single value or None

        if result is None:
            raise ValueError(
                f"No subject found for grade ID {student_grade_id} at offset {offset}"
            )

        return result


class SectionFactory(BaseFactory[Section]):
    class Meta:
        model = Section

    grade_id: Any = LazyAttribute(
        lambda _: GradeModelFactory.get_existing_id(random.randint(1, 12))
    )
    section: Any = LazyAttribute(lambda _: random.choice(["A", "B", "C"]))


class STUDSemesterRecordFactory(BaseFactory[STUDSemesterRecord]):
    class Meta:
        model = STUDSemesterRecord

    student_id: Any = LazyAttribute(lambda _: StudentFactory.get_or_create().id)
    semester_id: Any = LazyAttribute(lambda _: SemesterFactory.get_or_create().id)
    section_id: Any = LazyAttribute(
        lambda obj: SectionFactory.get_or_create(
            grade_id=StudentFactory.get_or_create(id=obj.student_id).current_grade_id,
            section=random.choice(["A", "B", "C"]),
        ).id
    )
    year_record_id: Any = LazyAttribute(
        lambda obj: YearRecordFactory.get_or_create(student_id=obj.student_id).id
    )
    average: Any = LazyAttribute(lambda _: random.uniform(40.0, 100.0))
    rank: Any = LazyAttribute(lambda _: random.randint(1, 50))


class YearRecordFactory(BaseFactory[STUDYearRecord]):
    class Meta:
        model = STUDYearRecord

    student_id: Any = LazyAttribute(lambda _: StudentFactory.get_or_create().id)
    grade_id: Any = LazyAttribute(
        lambda obj: StudentFactory.get_or_create(id=obj.student_id).current_grade_id
    )
    year_id: Any = LazyAttribute(lambda _: YearModelFactory.get_existing_id())
    final_score: Any = LazyAttribute(lambda _: random.uniform(40.0, 100.0))
    rank: Any = LazyAttribute(lambda _: random.randint(1, 50))


class AssessmentFactory(BaseFactory[Assessment]):
    class Meta:
        model = Assessment

    _skip_fields: List[str] = ["offset", "semester_id"]

    offset = factory.Sequence(lambda n: n)
    semester_id: Any = LazyAttribute(
        lambda _: SemesterFactory.get_or_create(name=1).id
    )  # Default to first semester

    student_id: Any = LazyAttribute(lambda _: StudentFactory.get_or_create().id)
    subject_id: Any = LazyAttribute(
        lambda obj: SubjectFactory.get_existing_id(
            student_grade_id=StudentFactory.get_or_create(
                id=obj.student_id
            ).current_grade_id,
            offset=obj.offset,
        )
    )  # Placeholder
    semester_record_id: Any = LazyAttribute(
        lambda obj: STUDSemesterRecordFactory.get_or_create(
            student_id=obj.student_id, semester_id=obj.semester_id
        ).id
    )
    teachers_record_id: Any = None  # Placeholder, can be set later


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
    subjects: List[Any]
    assessment_type: List[Any]


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

    type: Any = LazyAttribute(lambda _: random.choice(["Mid", "Final"]))
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


@dataclass
class SortQuery:
    tableId: str
    id: str
    desc: bool = False


@dataclass
class FilterQuery:
    id: str
    tableId: str
    variant: str
    operator: str
    value: Any


@dataclass
class SearchParams:
    page: int
    per_page: int
    join_operator: str
    sort_test_ids: str
    sort: List[SortQuery] = field(default_factory=list)
    filters: List[FilterQuery] = field(default_factory=list)


@dataclass
class QueryResponse:
    columns: List[str]
    search_params: SearchParams
    table_name: Optional[str] = None


class SortQueryFactory(TypedFactory[SortQuery]):
    class Meta:
        model = SortQuery
        exclude = ("sort_for",)

    # general fields helping defining others
    sort_for: Any = LazyAttribute(lambda _: None)

    id: Any = LazyAttribute(lambda x: next(iter(x.sort_for.items()))[0])
    tableId: Any = LazyAttribute(lambda x: next(iter(x.sort_for.items()))[1])
    desc: Any = LazyAttribute(lambda _: fake.boolean())

    def __init__(self, *args: Any, **kwargs: Any) -> Any:
        sort_for = kwargs.get("sort_for", self.sort_for)
        if not sort_for:
            raise ValueError("sort_for is required and cannot be None")

        # Call the parent constructor
        super().__init__(*args, **kwargs)


OPERATOR_CONFIG = {
    "text": ["iLike", "notLike", "startsWith", "endWith", "eq"],
    "number": ["eq", "ne", "lt", "lte", "gt", "gte"],
    "select": ["eq", "ne", "isEmpty", "isNotEmpty"],
    "multiSelect": ["in", "notIn", "isEmpty", "isNotEmpty"],
    "range": ["isBetween", "isNotBetween"],
    "date": [
        "eq",
        "ne",
        "lt",
        "lte",
        "gt",
        "gte",
        "isBetween",
        "isRelativeToToday",
        "isEmpty",
        "isNotEmpty",
    ],
    "dateRange": [
        "eq",
        "ne",
        "lt",
        "lte",
        "gt",
        "gte",
        "isBetween",
        "isRelativeToToday",
        "isEmpty",
        "isNotEmpty",
    ],
    "boolean": ["eq", "ne"],
}


@dataclass
class Variant:
    value: str

    def __post_init__(self):
        if self.value not in OPERATOR_CONFIG:
            raise ValueError(
                f"Invalid value '{self.value}'. Must be one of {list(OPERATOR_CONFIG)}"
            )


class variantFactory(TypedFactory[Variant]):
    class Meta:
        model = Variant
        exclude = ("variant_for", "variants")

    # general fields helping defining others
    variant_for: Any = LazyAttribute(lambda _: None)
    variants: Any = LazyAttribute(
        lambda _: {
            "identification": ["text"],
            "createdAt": ["dateRange"],
            "firstName_fatherName_grandFatherName": ["text"],
            "guardianName": ["text"],
            "guardianPhone": ["text"],
            "isActive": ["boolean"],
            "grade": ["multiSelect"],
            "sectionSemesterOne": ["multiSelect"],
            "sectionSemesterTwo": ["multiSelect"],
            "averageSemesterOne": ["multiSelect"],
            "averageSemesterTwo": ["multiSelect"],
            "rankSemesterOne": ["multiSelect"],
            "rankSemesterTwo": ["multiSelect"],
            "finalScore": ["multiSelect"],
            "rank": ["multiSelect"],
        }
    )
    value: Any = LazyAttribute(
        lambda obj: random.choice(obj.variants.get(obj.variant_for, []))
    )


@dataclass
class Value:
    identification: str
    createdAt: str
    firstName_fatherName_grandFatherName: str
    guardianName: str
    guardianPhone: str
    isActive: str
    grade: str
    sectionSemesterOne: str
    sectionSemesterTwo: str
    averageSemesterOne: str
    averageSemesterTwo: str
    rankSemesterOne: str
    rankSemesterTwo: str
    finalScore: str
    rank: str


class TableIdFactory(TypedFactory[Value]):
    class Meta:
        model = Value
        exclude = ("db_table",)

    db_table: Any = LazyAttribute(
        lambda _: {
            name: id for name, id in storage.session.query(Table.name, Table.id).all()
        }
    )

    identification: Any = LazyAttribute(lambda x: x.db_table["users"])
    firstName_fatherName_grandFatherName: Any = LazyAttribute(
        lambda x: x.db_table["students"]
    )
    guardianName: Any = LazyAttribute(lambda x: x.db_table["students"])
    guardianPhone: Any = LazyAttribute(lambda x: x.db_table["students"])
    isActive: Any = LazyAttribute(lambda x: x.db_table["students"])

    grade: Any = LazyAttribute(lambda x: x.db_table["grades"])
    sectionSemesterOne: Any = LazyAttribute(lambda x: x.db_table["sections"])
    sectionSemesterTwo: Any = LazyAttribute(lambda x: x.db_table["sections"])
    createdAt: Any = LazyAttribute(lambda x: x.db_table["users"])
    averageSemesterOne: Any = LazyAttribute(
        lambda x: x.db_table["student_semester_records"]
    )
    averageSemesterTwo: Any = LazyAttribute(
        lambda x: x.db_table["student_semester_records"]
    )
    rankSemesterOne: Any = LazyAttribute(
        lambda x: x.db_table["student_semester_records"]
    )
    rankSemesterTwo: Any = LazyAttribute(
        lambda x: x.db_table["student_semester_records"]
    )
    finalScore: Any = LazyAttribute(lambda x: x.db_table["student_year_records"])
    rank: Any = LazyAttribute(lambda x: x.db_table["student_year_records"])


@dataclass
class MinMax:
    min: Optional[float | int] = None
    max: Optional[float | int] = None

    def __post_init__(self):
        if self.min is not None and self.max is not None and self.min > self.max:
            raise ValueError("min cannot be greater than max")


# Helper for MinMaxFactory
MINMAX_GENERATE: Dict[type, Callable[[int, int], Any]] = {
    int: lambda x, y: random.randint(x, y),
    float: lambda x, y: round(random.uniform(x, y), 2),
    date: lambda x, y: str(
        fake.date_between(
            x if isinstance(x, date) else datetime.strptime(str(x), "%Y-%m-%d").date(),
            y if isinstance(y, date) else datetime.strptime(str(y), "%Y-%m-%d").date(),
        )
    ),
}


class MinMaxFactory(TypedFactory[MinMax]):
    class Meta:
        model = MinMax
        exclude = ("type", "lowest", "highest")

    # general fields helping defining others
    type: Any = LazyAttribute(lambda _: None)
    lowest: Any = LazyAttribute(lambda _: 0)
    highest: Any = LazyAttribute(lambda _: 100)

    min: Any = LazyAttribute(lambda x: MINMAX_GENERATE.get(x.type)(x.lowest, x.highest))
    max: Any = LazyAttribute(lambda x: MINMAX_GENERATE.get(x.type)(x.min, x.highest))


class valueFactory(TypedFactory[Value]):
    class Meta:
        model = Value

    identification: Any = LazyAttribute(lambda _: "MAS/100/23")
    firstName_fatherName_grandFatherName: Any = LazyAttribute(lambda _: fake.name())
    guardianName: Any = LazyAttribute(lambda _: fake.name())
    guardianPhone: Any = LazyAttribute(lambda _: "091234567")
    isActive: Any = LazyAttribute(lambda _: fake.boolean())
    grade: Any = LazyAttribute(
        lambda _: random.sample(range(1, 11), random.randint(1, 10))
    )
    sectionSemesterOne: Any = LazyAttribute(
        lambda _: random.sample(["A", "B", "C"], random.randint(1, 3))
    )
    sectionSemesterTwo: Any = LazyAttribute(
        lambda _: random.sample(["A", "B", "C"], random.randint(1, 3))
    )
    createdAt: Any = LazyAttribute(
        lambda _: MinMaxFactory(
            type=date, lowest=fake.past_date(), highest=fake.future_date()
        )
    )
    averageSemesterOne: Any = LazyAttribute(lambda _: MinMaxFactory(type=float))
    averageSemesterTwo: Any = LazyAttribute(lambda _: MinMaxFactory(type=float))
    rankSemesterOne: Any = LazyAttribute(
        lambda _: MinMaxFactory(type=int, lowest=1, highest=3)
    )
    rankSemesterTwo: Any = LazyAttribute(
        lambda _: MinMaxFactory(type=int, lowest=1, highest=3)
    )
    finalScore: Any = LazyAttribute(lambda _: MinMaxFactory(type=float))
    rank: Any = LazyAttribute(lambda _: MinMaxFactory(type=int, lowest=1, highest=3))


class FilterQueryFactory(TypedFactory[FilterQuery]):
    class Meta:
        model = FilterQuery
        exclude = ("filter_for",)

    # general fields helping defining others
    filter_for: Any = LazyAttribute(lambda _: None)

    id: Any = LazyAttribute(lambda x: next(iter(x.filter_for.items()))[0])
    tableId: Any = LazyAttribute(lambda x: next(iter(x.filter_for.items()))[1])
    variant: Any = LazyAttribute(lambda x: variantFactory(variant_for=x.id).value)
    operator: Any = LazyAttribute(
        lambda x: random.choice(OPERATOR_CONFIG.get(x.variant, []))
    )

    value: Any = LazyAttribute(lambda x: getattr(valueFactory(), x.id))

    def __init__(self, *args: Any, **kwargs: Any) -> Any:
        filter_for = kwargs.get("filter_for", self.filter_for)
        if not filter_for:
            raise ValueError("filter_for is required and cannot be None")

        # Call the parent constructor
        super().__init__(*args, **kwargs)


class RandomNoRepeat:
    def __init__(self, values: List[Any]) -> None:
        self.original = values[:]
        self.remaining = values[:]

    def __call__(self):
        if not self.remaining:
            # Optionally, you can reset here
            self.remaining = self.original[:]
            # Or raise an error: raise StopIteration("No more values to return.")

        choice = random.choice(self.remaining)
        self.remaining.remove(choice)
        return choice


class SearchParamsFactory(TypedFactory[SearchParams]):
    class Meta:
        model = SearchParams
        exclude = (
            "tableId",
            "get_sort",
            "get_filter",
            "create_sort",
            "create_filter",
            "sort_many",
            "filters_many",
        )

    @staticmethod
    def generate_sort_queries(tableId: Dict[str, str], create: int) -> List[SortQuery]:
        picker = RandomNoRepeat(list(tableId.items()))

        queries: List[SortQuery] = []
        for _ in range(create):
            random_pair = picker()
            sort_for = dict([random_pair])
            queries.append(SortQueryFactory.create(sort_for=sort_for))

        return queries

    # general fields helping defining others
    tableId: Any = LazyAttribute(lambda _: None)
    get_sort: Any = LazyAttribute(lambda _: False)
    get_filter: Any = LazyAttribute(lambda _: False)
    sort_many: Any = LazyAttribute(lambda _: False)
    filters_many: Any = LazyAttribute(lambda _: False)
    create_sort: Any = LazyAttribute(
        lambda x: random.randint(1, len(x.tableId)) if x.sort_many else 1
    )
    create_filter: Any = LazyAttribute(
        lambda x: random.randint(1, len(x.tableId)) if x.filters_many else 1
    )

    page: Any = LazyAttribute(lambda _: 1)
    per_page: Any = LazyAttribute(lambda _: random.choice([10, 20, 30, 40, 50]))
    join_operator: Any = LazyAttribute(lambda _: random.choice(["and", "or"]))
    sort: Any = LazyAttribute(
        lambda obj: SearchParamsFactory.generate_sort_queries(
            obj.tableId, obj.create_sort
        )
        if obj.get_sort
        else []
    )
    filters: Any = LazyAttribute(
        lambda obj: [
            FilterQueryFactory(
                filter_for=dict([random.choice(list(obj.tableId.items()))]),
            )
            for _ in range(obj.create_filter)
        ]
        if obj.get_filter
        else []
    )

    sort_test_ids: Any = LazyAttribute(
        lambda x: ", ".join(f"{s.id}-{'desc' if s.desc else 'asc'}" for s in x.sort)
    )


class QueryFactory(TypedFactory[QueryResponse]):
    class Meta:
        model = QueryResponse
        exclude = ("tableId",)

    # general fields helping defining others
    tableId: Any = LazyAttribute(lambda _: None)

    table_name: Any = LazyAttribute(lambda _: "students")
    columns: Any = LazyAttribute(
        lambda obj: random.sample(
            list(obj.tableId.keys()), random.randint(1, len(obj.tableId))
        )
    )
    search_params: Any = LazyAttribute(
        lambda obj: SearchParamsFactory.create(tableId=obj.tableId)
    )

    def __init__(self, *args: Any, **kwargs: Any) -> Any:
        tableId = kwargs.get("tableId", self.tableId)
        if not tableId:
            raise ValueError("tableId is required and cannot be None")

        # Call the parent constructor
        super().__init__(*args, **kwargs)
