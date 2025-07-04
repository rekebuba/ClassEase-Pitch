import random
from typing import Any, Sequence
from factory import LazyAttribute, SubFactory, post_generation
from faker import Faker
from sqlalchemy import select
from sqlmodel import col
from models.teacher import Teacher
from models import storage
from tests.test_api.factories.subject_factory import SubjectFactory
from .base_factory import BaseFactory
from .user_factory import UserFactory
from extension.enums.enum import (
    ExperienceYearEnum,
    GenderEnum,
    HighestDegreeEnum,
    MaritalStatusEnum,
    RoleEnum,
    ScheduleEnum,
)
from models.yearly_subject import YearlySubject

fake = Faker()


class TeacherFactory(BaseFactory[Teacher]):
    class Meta:
        model = Teacher
        sqlalchemy_session = storage.session
        exclude = ("user", "for_session")

    for_session: Any = False
    grade_level: Any = []
    subjects_to_teach: Any = []

    @post_generation
    def subject_and_grade_to_teach(self, create, extracted, **kwargs):
        if not create:
            return
        subjects = SubjectFactory.create_batch(size=random.randint(1, 3))
        self.subjects_to_teach.extend(subjects)

        yearly_subject = storage.session.scalars(
            select(YearlySubject)
            .where(
                col(YearlySubject.subject_id).in_([subject.id for subject in subjects])
            )
            .distinct()
        ).all()

        self.grade_level.extend(
            yearly_subject.grade for yearly_subject in yearly_subject
        )

    user: Any = SubFactory(UserFactory, role=RoleEnum.TEACHER)
    user_id: Any = LazyAttribute(lambda x: x.user.id if x.user else None)

    # Add additional fields for Teacher
    first_name: Any = LazyAttribute(lambda x: fake.first_name())
    father_name: Any = LazyAttribute(lambda x: fake.last_name())
    grand_father_name: Any = LazyAttribute(lambda x: fake.first_name())
    date_of_birth: Any = LazyAttribute(lambda x: fake.date_of_birth())
    gender: Any = LazyAttribute(
        lambda x: random.choice(list(GenderEnum._value2member_map_))
    )
    nationality: Any = LazyAttribute(lambda x: fake.country())
    marital_status: Any = LazyAttribute(
        lambda x: random.choice(list(MaritalStatusEnum._value2member_map_))
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

    # Emergency Contact
    emergency_contact_name: Any = LazyAttribute(lambda x: fake.name())
    emergency_contact_relation: Any = LazyAttribute(
        lambda x: fake.random_element(
            elements=("Parent", "Sibling", "Spouse", "Friend", "Other")
        )
    )
    emergency_contact_phone: Any = LazyAttribute(lambda x: fake.phone_number())
    emergency_contact_email: Any = LazyAttribute(lambda x: fake.email())

    # Educational Background
    highest_degree: Any = LazyAttribute(
        lambda x: fake.random_element(list(HighestDegreeEnum._value2member_map_))
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
        lambda x: random.choice(list(ExperienceYearEnum._value2member_map_))
    )
    previous_schools: Any = LazyAttribute(
        lambda x: fake.text(max_nb_chars=60) if random.choice([True, False]) else None
    )

    preferred_schedule: Any = LazyAttribute(
        lambda x: fake.random_element(list(ScheduleEnum._value2member_map_))
    )

    # Professional Skills & Qualifications
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
