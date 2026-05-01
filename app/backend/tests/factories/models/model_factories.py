from __future__ import annotations

import random
from datetime import date, datetime, timedelta, timezone
from typing import Any

import factory
from faker import Faker

from project.models import (
    AcademicTerm,
    Admin,
    Assessment,
    AuditLog,
    AuthIdentity,
    AuthSession,
    BlacklistToken,
    Employee,
    EmployeeYearLink,
    Event,
    Grade,
    GradeSectionLink,
    GradeStreamLink,
    GradeStreamSubject,
    MarkList,
    MembershipRole,
    Parent,
    ParentStudentLink,
    Permission,
    Registration,
    Role,
    RolePermission,
    SavedQueryView,
    School,
    SchoolMembership,
    Section,
    Stream,
    Student,
    StudentAcademicTermLink,
    StudentGradeLink,
    StudentSectionLink,
    StudentStreamLink,
    StudentSubjectLink,
    StudentTermRecord,
    StudentYearLink,
    StudentYearRecord,
    Subject,
    SubjectYearlyAverage,
    Table,
    TeacherRecord,
    TeacherRecordLink,
    TransferRequest,
    User,
    Year,
    YearlySubject,
)
from project.utils.enum import (
    AcademicTermEnum,
    AcademicTermTypeEnum,
    AcademicYearStatusEnum,
    AuthProviderEnum,
    AuthSessionAssuranceEnum,
    BloodTypeEnum,
    EmployeeApplicationStatusEnum,
    EmployeePositionEnum,
    EventEligibilityEnum,
    EventLocationEnum,
    EventOrganizerEnum,
    EventPurposeEnum,
    ExperienceYearEnum,
    GenderEnum,
    GradeEnum,
    GradeLevelEnum,
    HighestEducationEnum,
    MarkListTypeEnum,
    MfaStateEnum,
    RoleEnum,
    SchoolMembershipStatusEnum,
    SchoolStatusEnum,
    StudentApplicationStatusEnum,
    TableEnum,
    TransferRequestStatusEnum,
)
from tests.factories.typed_factory import TypedFactory

fake = Faker()


def _pick(enum_cls: Any) -> Any:
    return random.choice(list(enum_cls))


class SchoolFactory(TypedFactory[School]):
    class Meta:
        model = School

    name = factory.Sequence(lambda n: f"{fake.company()}-{n}")
    slug = factory.Sequence(lambda n: f"school-{n}-{fake.slug()}")
    status = factory.LazyFunction(lambda: _pick(SchoolStatusEnum))
    domain = factory.LazyAttribute(lambda o: f"{o.slug}.example.com")
    logo_path = None
    primary_color = factory.Faker("hex_color")
    settings = factory.LazyFunction(lambda: {"timezone": "Africa/Nairobi"})

    class Params:
        with_membership = factory.Trait(
            membership=factory.RelatedFactory(
                "tests.factories.models.model_factories.SchoolMembershipFactory",
                factory_related_name="school_obj",
            )
        )
        with_year = factory.Trait(
            year=factory.RelatedFactory(
                "tests.factories.models.model_factories.YearFactory",
                factory_related_name="school_obj",
            )
        )


class UserFactory(TypedFactory[User]):
    class Meta:
        model = User

    membership_id = None
    role = factory.LazyFunction(lambda: _pick(RoleEnum))
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    phone = factory.Sequence(lambda n: f"+2519000{n:06d}")
    username = factory.Sequence(lambda n: f"user-{n}")
    image_path = factory.LazyFunction(lambda: fake.file_path(depth=2, extension="jpg"))
    is_active = True
    is_verified = True

    class Params:
        with_membership = factory.Trait(
            membership=factory.RelatedFactory(
                "tests.factories.models.model_factories.SchoolMembershipFactory",
                factory_related_name="user_obj",
            )
        )
        as_admin = factory.Trait(
            role=RoleEnum.ADMIN,
            admin_profile=factory.RelatedFactory(
                "tests.factories.models.model_factories.AdminFactory",
                factory_related_name="user_obj",
            ),
        )
        as_employee = factory.Trait(
            role=RoleEnum.TEACHER,
            employee_profile=factory.RelatedFactory(
                "tests.factories.models.model_factories.EmployeeFactory",
                factory_related_name="user_obj",
            ),
        )
        as_student = factory.Trait(
            role=RoleEnum.STUDENT,
            student_profile=factory.RelatedFactory(
                "tests.factories.models.model_factories.StudentFactory",
                factory_related_name="user_obj",
            ),
        )
        as_parent = factory.Trait(
            role=RoleEnum.PARENT,
            parent_profile=factory.RelatedFactory(
                "tests.factories.models.model_factories.ParentFactory",
                factory_related_name="user_obj",
            ),
        )


class YearFactory(TypedFactory[Year]):
    class Meta:
        model = Year
        exclude = ("school_obj",)

    school_obj = factory.SubFactory(SchoolFactory)
    calendar_type = factory.LazyFunction(lambda: _pick(AcademicTermTypeEnum))
    name = factory.Sequence(lambda n: f"Academic Year {2020 + n}/{2021 + n}")
    start_date = factory.LazyFunction(lambda: date.today())
    end_date = factory.LazyAttribute(lambda o: o.start_date + timedelta(days=270))
    status = factory.LazyFunction(lambda: _pick(AcademicYearStatusEnum))

    class Params:
        with_term = factory.Trait(
            term=factory.RelatedFactory(
                "tests.factories.models.model_factories.AcademicTermFactory",
                factory_related_name="year_obj",
            )
        )
        with_grade = factory.Trait(
            grade=factory.RelatedFactory(
                "tests.factories.models.model_factories.GradeFactory",
                factory_related_name="year_obj",
            )
        )


class GradeFactory(TypedFactory[Grade]):
    class Meta:
        model = Grade
        exclude = ("year_obj",)

    year_obj = factory.SubFactory(YearFactory)
    year_id = factory.LazyAttribute(lambda o: o.year_obj.id)
    grade = factory.LazyFunction(lambda: _pick(GradeEnum))
    level = factory.LazyFunction(lambda: _pick(GradeLevelEnum))
    has_stream = False

    class Params:
        with_stream = factory.Trait(
            has_stream=True,
            stream=factory.RelatedFactory(
                "tests.factories.models.model_factories.StreamFactory",
                factory_related_name="grade_obj",
            ),
        )
        with_section = factory.Trait(
            section_obj=factory.RelatedFactory(
                "tests.factories.models.model_factories.SectionFactory",
                factory_related_name="grade_obj",
            )
        )


class StreamFactory(TypedFactory[Stream]):
    class Meta:
        model = Stream
        exclude = ("grade_obj",)

    grade_obj = factory.SubFactory(GradeFactory, has_stream=True)
    grade_id = factory.LazyAttribute(lambda o: o.grade_obj.id)
    name = factory.Sequence(lambda n: f"Stream-{n}")


class SectionFactory(TypedFactory[Section]):
    class Meta:
        model = Section
        exclude = ("grade_obj",)

    grade_obj = factory.SubFactory(GradeFactory)
    grade_id = factory.LazyAttribute(lambda o: o.grade_obj.id)
    section = factory.Sequence(lambda n: chr(65 + (n % 26)))


class SubjectFactory(TypedFactory[Subject]):
    class Meta:
        model = Subject
        exclude = ("year_obj",)

    year_obj = factory.SubFactory(YearFactory)
    year_id = factory.LazyAttribute(lambda o: o.year_obj.id)
    name = factory.Sequence(lambda n: f"Subject {n}")
    code = factory.Sequence(lambda n: f"SUB-{n:03d}")


class AcademicTermFactory(TypedFactory[AcademicTerm]):
    class Meta:
        model = AcademicTerm
        exclude = ("year_obj",)

    year_obj = factory.SubFactory(YearFactory)
    year_id = factory.LazyAttribute(lambda o: o.year_obj.id)
    name = factory.LazyFunction(lambda: _pick(AcademicTermEnum))
    start_date = factory.LazyFunction(lambda: date.today())
    end_date = factory.LazyAttribute(lambda o: o.start_date + timedelta(days=90))
    registration_start = factory.LazyAttribute(
        lambda o: o.start_date - timedelta(days=14)
    )
    registration_end = factory.LazyAttribute(lambda o: o.start_date + timedelta(days=7))


class SchoolMembershipFactory(TypedFactory[SchoolMembership]):
    class Meta:
        model = SchoolMembership
        exclude = ("user_obj", "school_obj")

    user_obj = factory.SubFactory(UserFactory)
    school_obj = factory.SubFactory(SchoolFactory)
    user_id = factory.LazyAttribute(lambda o: o.user_obj.id)
    school_id = factory.LazyAttribute(lambda o: o.school_obj.id)
    joined_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    status = SchoolMembershipStatusEnum.ACTIVE
    login_identifier = factory.Sequence(lambda n: f"member-{n}")
    left_at = None
    mfa_state = factory.LazyFunction(lambda: _pick(MfaStateEnum))
    is_primary = False
    permissions_version = 1

    class Params:
        with_role = factory.Trait(
            membership_role=factory.RelatedFactory(
                "tests.factories.models.model_factories.MembershipRoleFactory",
                factory_related_name="membership_obj",
            )
        )


class RoleFactory(TypedFactory[Role]):
    class Meta:
        model = Role
        exclude = ("school_obj",)

    school_obj = factory.SubFactory(SchoolFactory)
    school_id = factory.LazyAttribute(lambda o: o.school_obj.id)
    name = factory.Sequence(lambda n: f"role-{n}")
    description = factory.Faker("sentence", nb_words=6)
    is_system = False

    class Params:
        with_permission = factory.Trait(
            role_permission=factory.RelatedFactory(
                "tests.factories.models.model_factories.RolePermissionFactory",
                factory_related_name="role_obj",
            )
        )


class PermissionFactory(TypedFactory[Permission]):
    class Meta:
        model = Permission

    code = factory.Sequence(lambda n: f"perm.{n}")
    description = factory.Faker("sentence", nb_words=8)


class MembershipRoleFactory(TypedFactory[MembershipRole]):
    class Meta:
        model = MembershipRole
        exclude = ("membership_obj", "role_obj")

    membership_obj = factory.SubFactory(SchoolMembershipFactory)
    role_obj = factory.SubFactory(RoleFactory)
    membership_id = factory.LazyAttribute(lambda o: o.membership_obj.id)
    role_id = factory.LazyAttribute(lambda o: o.role_obj.id)


class RolePermissionFactory(TypedFactory[RolePermission]):
    class Meta:
        model = RolePermission
        exclude = ("role_obj", "permission_obj")

    role_obj = factory.SubFactory(RoleFactory)
    permission_obj = factory.SubFactory(PermissionFactory)
    role_id = factory.LazyAttribute(lambda o: o.role_obj.id)
    permission_id = factory.LazyAttribute(lambda o: o.permission_obj.id)


class AdminFactory(TypedFactory[Admin]):
    class Meta:
        model = Admin
        exclude = ("user_obj", "membership_obj")

    user_obj = factory.SubFactory(UserFactory, role=RoleEnum.ADMIN)
    membership_obj = factory.SubFactory(
        SchoolMembershipFactory,
        user_obj=factory.SelfAttribute("..user_obj"),
    )
    user_id = factory.LazyAttribute(lambda o: o.user_obj.id)
    school_membership_id = factory.LazyAttribute(lambda o: o.membership_obj.id)
    first_name = factory.Faker("first_name")
    father_name = factory.Faker("last_name")
    grand_father_name = factory.Faker("last_name")
    date_of_birth = factory.Faker("date_of_birth", minimum_age=25, maximum_age=65)
    gender = factory.LazyFunction(lambda: _pick(GenderEnum))


class EmployeeFactory(TypedFactory[Employee]):
    class Meta:
        model = Employee
        exclude = ("user_obj", "membership_obj", "subject_obj")

    user_obj = factory.SubFactory(UserFactory, role=RoleEnum.TEACHER)
    membership_obj = factory.SubFactory(
        SchoolMembershipFactory,
        user_obj=factory.SelfAttribute("..user_obj"),
    )
    subject_obj = factory.SubFactory(SubjectFactory)

    user_id = factory.LazyAttribute(lambda o: o.user_obj.id)
    school_membership_id = factory.LazyAttribute(lambda o: o.membership_obj.id)
    subject_id = factory.LazyAttribute(lambda o: o.subject_obj.id)

    first_name = factory.Faker("first_name")
    father_name = factory.Faker("last_name")
    grand_father_name = factory.Faker("last_name")
    date_of_birth = factory.Faker("date_of_birth", minimum_age=22, maximum_age=70)
    gender = factory.LazyFunction(lambda: _pick(GenderEnum))
    nationality = factory.Faker("country")
    social_security_number = factory.Sequence(lambda n: f"SSN-{n:08d}")
    city = factory.Faker("city")
    state = factory.Faker("state")
    country = factory.Faker("country")
    emergency_contact_name = factory.Faker("name")
    emergency_contact_relation = factory.LazyFunction(
        lambda: random.choice(["Spouse", "Sibling", "Parent"])
    )
    emergency_contact_phone = factory.Sequence(lambda n: f"+251911{n:06d}")
    highest_education = factory.LazyFunction(lambda: _pick(HighestEducationEnum))
    university = factory.Faker("company")
    graduation_year = factory.LazyFunction(lambda: random.randint(1998, 2024))
    gpa = factory.LazyFunction(lambda: round(random.uniform(2.0, 4.0), 2))
    position = factory.LazyFunction(lambda: _pick(EmployeePositionEnum))
    years_of_experience = factory.LazyFunction(lambda: _pick(ExperienceYearEnum))
    secondary_phone = factory.Sequence(lambda n: f"+251922{n:06d}")
    certifications = factory.Faker("sentence", nb_words=5)
    resume = factory.LazyFunction(lambda: fake.file_name(extension="pdf"))
    status = EmployeeApplicationStatusEnum.PENDING

    class Params:
        without_subject = factory.Trait(subject_obj=None, subject_id=None)


class ParentFactory(TypedFactory[Parent]):
    class Meta:
        model = Parent
        exclude = ("user_obj", "membership_obj")

    user_obj = factory.SubFactory(UserFactory, role=RoleEnum.PARENT)
    membership_obj = factory.SubFactory(
        SchoolMembershipFactory,
        user_obj=factory.SelfAttribute("..user_obj"),
    )

    user_id = factory.LazyAttribute(lambda o: o.user_obj.id)
    school_membership_id = factory.LazyAttribute(lambda o: o.membership_obj.id)

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    gender = factory.LazyFunction(lambda: _pick(GenderEnum))
    email = factory.Sequence(lambda n: f"parent{n}@example.com")
    phone = factory.Sequence(lambda n: f"+251933{n:06d}")
    relation = factory.LazyFunction(
        lambda: random.choice(["mother", "father", "guardian"])
    )
    emergency_contact_phone = factory.Sequence(lambda n: f"+251944{n:06d}")


class StudentFactory(TypedFactory[Student]):
    class Meta:
        model = Student
        exclude = ("user_obj", "membership_obj", "grade_obj")

    grade_obj = factory.SubFactory(GradeFactory)
    user_obj = factory.SubFactory(UserFactory, role=RoleEnum.STUDENT)
    membership_obj = factory.SubFactory(
        SchoolMembershipFactory,
        user_obj=factory.SelfAttribute("..user_obj"),
    )

    registered_for_grade_id = factory.LazyAttribute(lambda o: o.grade_obj.id)
    user_id = factory.LazyAttribute(lambda o: o.user_obj.id)
    school_membership_id = factory.LazyAttribute(lambda o: o.membership_obj.id)

    first_name = factory.Faker("first_name")
    father_name = factory.Faker("last_name")
    grand_father_name = factory.Faker("last_name")
    date_of_birth = factory.Faker("date_of_birth", minimum_age=6, maximum_age=19)
    gender = factory.LazyFunction(lambda: _pick(GenderEnum))
    city = factory.Faker("city")
    state = factory.Faker("state")
    postal_code = factory.Faker("postcode")
    nationality = factory.Faker("country")
    blood_type = factory.LazyFunction(lambda: _pick(BloodTypeEnum))
    student_photo = factory.LazyFunction(lambda: fake.file_name(extension="jpg"))
    previous_school = factory.LazyFunction(lambda: fake.company())
    transportation = factory.LazyFunction(
        lambda: random.choice(["bus", "walk", "parent"])
    )
    disability_details = None
    medical_details = None
    has_medical_condition = False
    has_disability = False
    is_transfer = False
    status = StudentApplicationStatusEnum.PENDING

    class Params:
        transfer_student = factory.Trait(
            is_transfer=True,
            previous_school=factory.Faker("company"),
        )


class EventFactory(TypedFactory[Event]):
    class Meta:
        model = Event
        exclude = ("year_obj",)

    year_obj = factory.SubFactory(YearFactory)
    year_id = factory.LazyAttribute(lambda o: o.year_obj.id)
    title = factory.Faker("sentence", nb_words=4)
    purpose = factory.LazyFunction(lambda: _pick(EventPurposeEnum))
    organizer = factory.LazyFunction(lambda: _pick(EventOrganizerEnum))
    start_date = factory.LazyFunction(lambda: date.today() + timedelta(days=5))
    end_date = factory.LazyAttribute(lambda o: o.start_date + timedelta(days=1))
    start_time = factory.LazyFunction(lambda: datetime.now().replace(microsecond=0))
    end_time = factory.LazyAttribute(lambda o: o.start_time + timedelta(hours=2))
    location = factory.LazyFunction(lambda: _pick(EventLocationEnum))
    is_hybrid = False
    online_link = None
    eligibility = factory.LazyFunction(lambda: _pick(EventEligibilityEnum))
    has_fee = False
    fee_amount = 0
    description = factory.Faker("sentence", nb_words=10)

    class Params:
        hybrid = factory.Trait(
            is_hybrid=True,
            online_link=factory.Faker("url"),
        )
        paid = factory.Trait(
            has_fee=True,
            fee_amount=250,
        )


class GradeStreamSubjectFactory(TypedFactory[GradeStreamSubject]):
    class Meta:
        model = GradeStreamSubject
        exclude = ("grade_obj", "stream_obj", "subject_obj")

    grade_obj = factory.SubFactory(GradeFactory, has_stream=True)
    stream_obj = factory.SubFactory(
        StreamFactory,
        grade_obj=factory.SelfAttribute("..grade_obj"),
    )
    subject_obj = factory.SubFactory(
        SubjectFactory,
    )

    grade_id = factory.LazyAttribute(lambda o: o.grade_obj.id)
    stream_id = factory.LazyAttribute(
        lambda o: o.stream_obj.id if o.stream_obj else None
    )
    subject_id = factory.LazyAttribute(lambda o: o.subject_obj.id)

    class Params:
        no_stream = factory.Trait(stream_obj=None, stream_id=None)


class TeacherRecordFactory(TypedFactory[TeacherRecord]):
    class Meta:
        model = TeacherRecord
        exclude = ("employee_obj", "academic_term_obj", "grade_stream_subject_obj")

    employee_obj = factory.SubFactory(EmployeeFactory)
    academic_term_obj = factory.SubFactory(AcademicTermFactory)
    grade_stream_subject_obj = factory.SubFactory(
        GradeStreamSubjectFactory,
        grade_obj=factory.SubFactory(GradeFactory),
    )

    employee_id = factory.LazyAttribute(lambda o: o.employee_obj.id)
    academic_term_id = factory.LazyAttribute(lambda o: o.academic_term_obj.id)
    grade_stream_subject_id = factory.LazyAttribute(
        lambda o: o.grade_stream_subject_obj.id if o.grade_stream_subject_obj else None
    )

    class Params:
        unassigned_subject = factory.Trait(
            grade_stream_subject_obj=None,
            grade_stream_subject_id=None,
        )


class StudentTermRecordFactory(TypedFactory[StudentTermRecord]):
    class Meta:
        model = StudentTermRecord
        exclude = (
            "student_obj",
            "academic_term_obj",
            "grade_obj",
            "section_obj",
            "stream_obj",
        )

    student_obj = factory.SubFactory(StudentFactory)
    academic_term_obj = factory.SubFactory(
        AcademicTermFactory,
    )
    grade_obj = factory.SubFactory(GradeFactory)
    section_obj = factory.SubFactory(
        SectionFactory, grade_obj=factory.SelfAttribute("..grade_obj")
    )
    stream_obj = factory.SubFactory(
        StreamFactory, grade_obj=factory.SelfAttribute("..grade_obj")
    )

    student_id = factory.LazyAttribute(lambda o: o.student_obj.id)
    academic_term_id = factory.LazyAttribute(lambda o: o.academic_term_obj.id)
    grade_id = factory.LazyAttribute(lambda o: o.grade_obj.id)
    section_id = factory.LazyAttribute(lambda o: o.section_obj.id)
    stream_id = factory.LazyAttribute(
        lambda o: o.stream_obj.id if o.stream_obj else None
    )
    average = factory.LazyFunction(lambda: round(random.uniform(50, 100), 2))
    rank = factory.LazyFunction(lambda: random.randint(1, 50))

    class Params:
        no_stream = factory.Trait(stream_obj=None, stream_id=None)


class MarkListFactory(TypedFactory[MarkList]):
    class Meta:
        model = MarkList
        exclude = ("student_obj", "student_term_record_obj", "subject_obj")

    student_obj = factory.SubFactory(StudentFactory)
    student_term_record_obj = factory.SubFactory(
        StudentTermRecordFactory,
        student_obj=factory.SelfAttribute("..student_obj"),
    )
    subject_obj = factory.SubFactory(
        SubjectFactory,
    )

    student_id = factory.LazyAttribute(lambda o: o.student_obj.id)
    student_term_record_id = factory.LazyAttribute(
        lambda o: o.student_term_record_obj.id
    )
    subject_id = factory.LazyAttribute(lambda o: o.subject_obj.id)
    type = factory.LazyFunction(lambda: _pick(MarkListTypeEnum))
    percentage = factory.LazyFunction(lambda: random.choice([10, 15, 20, 25, 30]))
    score = factory.LazyFunction(lambda: round(random.uniform(40, 100), 2))


class YearlySubjectFactory(TypedFactory[YearlySubject]):
    class Meta:
        model = YearlySubject
        exclude = ("year_obj", "subject_obj", "grade_obj", "stream_obj")

    year_obj = factory.SubFactory(YearFactory)
    grade_obj = factory.SubFactory(
        GradeFactory, year_obj=factory.SelfAttribute("..year_obj")
    )
    stream_obj = factory.SubFactory(
        StreamFactory, grade_obj=factory.SelfAttribute("..grade_obj")
    )
    subject_obj = factory.SubFactory(
        SubjectFactory, year_obj=factory.SelfAttribute("..year_obj")
    )

    subject_code = factory.LazyAttribute(lambda o: o.subject_obj.code)
    year_id = factory.LazyAttribute(lambda o: o.year_obj.id)
    subject_id = factory.LazyAttribute(lambda o: o.subject_obj.id)
    grade_id = factory.LazyAttribute(lambda o: o.grade_obj.id)
    stream_id = factory.LazyAttribute(
        lambda o: o.stream_obj.id if o.stream_obj else None
    )

    class Params:
        no_stream = factory.Trait(stream_obj=None, stream_id=None)


class AssessmentFactory(TypedFactory[Assessment]):
    class Meta:
        model = Assessment
        exclude = ("student_obj", "student_term_record_obj", "yearly_subject_obj")

    student_obj = factory.SubFactory(StudentFactory)
    student_term_record_obj = factory.SubFactory(
        StudentTermRecordFactory,
        student_obj=factory.SelfAttribute("..student_obj"),
    )
    yearly_subject_obj = factory.SubFactory(
        YearlySubjectFactory,
    )

    student_id = factory.LazyAttribute(lambda o: o.student_obj.id)
    student_term_record_id = factory.LazyAttribute(
        lambda o: o.student_term_record_obj.id
    )
    yearly_subject_id = factory.LazyAttribute(lambda o: o.yearly_subject_obj.id)
    total = factory.LazyFunction(lambda: round(random.uniform(300, 700), 2))
    rank = factory.LazyFunction(lambda: random.randint(1, 50))


class SubjectYearlyAverageFactory(TypedFactory[SubjectYearlyAverage]):
    class Meta:
        model = SubjectYearlyAverage
        exclude = ("student_obj", "yearly_subject_obj", "student_year_record_obj")

    student_obj = factory.SubFactory(StudentFactory)
    yearly_subject_obj = factory.SubFactory(
        YearlySubjectFactory,
    )
    student_year_record_obj = factory.SubFactory(
        "tests.factories.models.model_factories.StudentYearRecordFactory",
        student_obj=factory.SelfAttribute("..student_obj"),
    )

    student_id = factory.LazyAttribute(lambda o: o.student_obj.id)
    yearly_subject_id = factory.LazyAttribute(lambda o: o.yearly_subject_obj.id)
    student_year_record_id = factory.LazyAttribute(
        lambda o: o.student_year_record_obj.id if o.student_year_record_obj else None
    )
    average = factory.LazyFunction(lambda: round(random.uniform(50, 100), 2))
    rank = factory.LazyFunction(lambda: random.randint(1, 50))

    class Params:
        without_year_record = factory.Trait(
            student_year_record_obj=None,
            student_year_record_id=None,
        )


class SavedQueryViewFactory(TypedFactory[SavedQueryView]):
    class Meta:
        model = SavedQueryView
        exclude = ("user_obj",)

    user_obj = factory.SubFactory(UserFactory)
    user_id = factory.LazyAttribute(lambda o: o.user_obj.id)
    name = factory.Sequence(lambda n: f"Saved Query {n}")
    table_name = factory.LazyFunction(lambda: _pick(TableEnum))
    query_json = factory.LazyFunction(lambda: {"filters": [], "columns": ["id"]})


class AuthIdentityFactory(TypedFactory[AuthIdentity]):
    class Meta:
        model = AuthIdentity
        exclude = ("user_obj",)

    user_obj = factory.SubFactory(UserFactory)
    user_id = factory.LazyAttribute(lambda o: o.user_obj.id)
    provider = AuthProviderEnum.PASSWORD
    provider_user_id = factory.Sequence(lambda n: f"provider-user-{n}")
    password = factory.Faker("password", length=18)

    class Params:
        google = factory.Trait(
            provider=AuthProviderEnum.GOOGLE,
            password=None,
        )


class AuthSessionFactory(TypedFactory[AuthSession]):
    class Meta:
        model = AuthSession
        exclude = ("user_obj", "school_obj", "membership_obj")

    user_obj = factory.SubFactory(UserFactory)
    school_obj = factory.SubFactory(SchoolFactory)
    membership_obj = factory.SubFactory(
        SchoolMembershipFactory,
        user_obj=factory.SelfAttribute("..user_obj"),
        school_obj=factory.SelfAttribute("..school_obj"),
    )

    user_id = factory.LazyAttribute(lambda o: o.user_obj.id)
    school_id = factory.LazyAttribute(lambda o: o.school_obj.id)
    membership_id = factory.LazyAttribute(lambda o: o.membership_obj.id)
    refresh_token_hash = factory.Sequence(lambda n: f"refresh-token-hash-{n}")
    expires_at = factory.LazyFunction(
        lambda: datetime.now(timezone.utc) + timedelta(days=30)
    )
    last_seen_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    user_agent = factory.Faker("user_agent")
    ip_address = factory.Faker("ipv4")
    assurance_level = factory.LazyFunction(lambda: _pick(AuthSessionAssuranceEnum))
    revoked_at = None
    revoke_reason = None

    class Params:
        revoked = factory.Trait(
            revoked_at=factory.LazyFunction(lambda: datetime.now(timezone.utc)),
            revoke_reason="manual",
        )


class AuditLogFactory(TypedFactory[AuditLog]):
    class Meta:
        model = AuditLog
        exclude = ("school_obj", "user_obj", "membership_obj", "auth_session_obj")

    school_obj = factory.SubFactory(SchoolFactory)
    user_obj = factory.SubFactory(UserFactory)
    membership_obj = factory.SubFactory(
        SchoolMembershipFactory,
        user_obj=factory.SelfAttribute("..user_obj"),
        school_obj=factory.SelfAttribute("..school_obj"),
    )
    auth_session_obj = factory.SubFactory(
        AuthSessionFactory,
        user_obj=factory.SelfAttribute("..user_obj"),
        school_obj=factory.SelfAttribute("..school_obj"),
        membership_obj=factory.SelfAttribute("..membership_obj"),
    )

    school_id = factory.LazyAttribute(
        lambda o: o.school_obj.id if o.school_obj else None
    )
    user_id = factory.LazyAttribute(lambda o: o.user_obj.id if o.user_obj else None)
    membership_id = factory.LazyAttribute(
        lambda o: o.membership_obj.id if o.membership_obj else None
    )
    auth_session_id = factory.LazyAttribute(
        lambda o: o.auth_session_obj.id if o.auth_session_obj else None
    )
    action = factory.Faker("word")
    resource_type = factory.Faker("word")
    resource_id = factory.LazyFunction(lambda: str(fake.uuid4()))
    outcome = factory.LazyFunction(lambda: random.choice(["success", "failure"]))
    ip_address = factory.Faker("ipv4")
    user_agent = factory.Faker("user_agent")
    details = factory.LazyFunction(lambda: {"reason": fake.sentence(nb_words=6)})

    class Params:
        minimal = factory.Trait(
            school_obj=None,
            user_obj=None,
            membership_obj=None,
            auth_session_obj=None,
            school_id=None,
            user_id=None,
            membership_id=None,
            auth_session_id=None,
        )


class TransferRequestFactory(TypedFactory[TransferRequest]):
    class Meta:
        model = TransferRequest
        exclude = (
            "source_school_obj",
            "target_school_obj",
            "subject_user_obj",
            "requested_membership_obj",
            "reviewed_membership_obj",
        )

    source_school_obj = factory.SubFactory(SchoolFactory)
    target_school_obj = factory.SubFactory(SchoolFactory)
    subject_user_obj = factory.SubFactory(UserFactory)
    requested_membership_obj = factory.SubFactory(
        SchoolMembershipFactory,
        user_obj=factory.SelfAttribute("..subject_user_obj"),
        school_obj=factory.SelfAttribute("..source_school_obj"),
    )
    reviewed_membership_obj = factory.SubFactory(
        SchoolMembershipFactory,
        school_obj=factory.SelfAttribute("..target_school_obj"),
    )

    source_school_id = factory.LazyAttribute(lambda o: o.source_school_obj.id)
    target_school_id = factory.LazyAttribute(lambda o: o.target_school_obj.id)
    subject_user_id = factory.LazyAttribute(lambda o: o.subject_user_obj.id)
    record_scope = factory.LazyFunction(
        lambda: random.choice(["student", "employee", "full"])
    )
    requested_by_membership_id = factory.LazyAttribute(
        lambda o: o.requested_membership_obj.id if o.requested_membership_obj else None
    )
    reviewed_by_membership_id = factory.LazyAttribute(
        lambda o: o.reviewed_membership_obj.id if o.reviewed_membership_obj else None
    )
    status = TransferRequestStatusEnum.PENDING
    notes = factory.Faker("sentence", nb_words=10)
    payload = factory.LazyFunction(lambda: {"includeRecords": True})

    class Params:
        pending = factory.Trait(status=TransferRequestStatusEnum.PENDING)
        approved = factory.Trait(status=TransferRequestStatusEnum.APPROVED)
        rejected = factory.Trait(status=TransferRequestStatusEnum.REJECTED)


class RegistrationFactory(TypedFactory[Registration]):
    class Meta:
        model = Registration
        exclude = ("student_obj", "subject_obj")

    student_obj = factory.SubFactory(StudentFactory)
    subject_obj = factory.SubFactory(
        SubjectFactory,
    )

    student_id = factory.LazyAttribute(lambda o: o.student_obj.id)
    subject_id = factory.LazyAttribute(lambda o: o.subject_obj.id)
    registration_date = factory.LazyFunction(lambda: datetime.now())


class BlacklistTokenFactory(TypedFactory[BlacklistToken]):
    class Meta:
        model = BlacklistToken

    jti = factory.Sequence(lambda n: f"jti-{n}")


class TableFactory(TypedFactory[Table]):
    class Meta:
        model = Table

    name = factory.Sequence(lambda n: f"table_{n}")


class ParentStudentLinkFactory(TypedFactory[ParentStudentLink]):
    class Meta:
        model = ParentStudentLink
        exclude = ("parent_obj", "student_obj")

    parent_obj = factory.SubFactory(ParentFactory)
    student_obj = factory.SubFactory(StudentFactory)
    parent_id = factory.LazyAttribute(lambda o: o.parent_obj.id)
    student_id = factory.LazyAttribute(lambda o: o.student_obj.id)


class StudentYearLinkFactory(TypedFactory[StudentYearLink]):
    class Meta:
        model = StudentYearLink
        exclude = ("student_obj", "year_obj")

    student_obj = factory.SubFactory(StudentFactory)
    year_obj = factory.SubFactory(YearFactory)
    student_id = factory.LazyAttribute(lambda o: o.student_obj.id)
    year_id = factory.LazyAttribute(lambda o: o.year_obj.id)
    average = factory.LazyFunction(lambda: round(random.uniform(50, 100), 2))
    rank = factory.LazyFunction(lambda: random.randint(1, 50))


class StudentAcademicTermLinkFactory(TypedFactory[StudentAcademicTermLink]):
    class Meta:
        model = StudentAcademicTermLink
        exclude = ("student_obj", "academic_term_obj")

    student_obj = factory.SubFactory(StudentFactory)
    academic_term_obj = factory.SubFactory(
        AcademicTermFactory,
    )
    student_id = factory.LazyAttribute(lambda o: o.student_obj.id)
    academic_term_id = factory.LazyAttribute(lambda o: o.academic_term_obj.id)
    average = factory.LazyFunction(lambda: round(random.uniform(50, 100), 2))
    rank = factory.LazyFunction(lambda: random.randint(1, 50))


class StudentGradeLinkFactory(TypedFactory[StudentGradeLink]):
    class Meta:
        model = StudentGradeLink
        exclude = ("student_obj", "grade_obj")

    student_obj = factory.SubFactory(StudentFactory)
    grade_obj = factory.SubFactory(GradeFactory)
    student_id = factory.LazyAttribute(lambda o: o.student_obj.id)
    grade_id = factory.LazyAttribute(lambda o: o.grade_obj.id)


class StudentSectionLinkFactory(TypedFactory[StudentSectionLink]):
    class Meta:
        model = StudentSectionLink
        exclude = ("student_obj", "section_obj")

    student_obj = factory.SubFactory(StudentFactory)
    section_obj = factory.SubFactory(SectionFactory)
    student_id = factory.LazyAttribute(lambda o: o.student_obj.id)
    section_id = factory.LazyAttribute(lambda o: o.section_obj.id)


class StudentStreamLinkFactory(TypedFactory[StudentStreamLink]):
    class Meta:
        model = StudentStreamLink
        exclude = ("student_obj", "stream_obj")

    student_obj = factory.SubFactory(StudentFactory)
    stream_obj = factory.SubFactory(StreamFactory)
    student_id = factory.LazyAttribute(lambda o: o.student_obj.id)
    stream_id = factory.LazyAttribute(lambda o: o.stream_obj.id)


class StudentSubjectLinkFactory(TypedFactory[StudentSubjectLink]):
    class Meta:
        model = StudentSubjectLink
        exclude = ("student_obj", "subject_obj")

    student_obj = factory.SubFactory(StudentFactory)
    subject_obj = factory.SubFactory(SubjectFactory)
    student_id = factory.LazyAttribute(lambda o: o.student_obj.id)
    subject_id = factory.LazyAttribute(lambda o: o.subject_obj.id)
    average = factory.LazyFunction(lambda: round(random.uniform(50, 100), 2))
    rank = factory.LazyFunction(lambda: random.randint(1, 50))


class EmployeeYearLinkFactory(TypedFactory[EmployeeYearLink]):
    class Meta:
        model = EmployeeYearLink
        exclude = ("employee_obj", "year_obj")

    employee_obj = factory.SubFactory(EmployeeFactory)
    year_obj = factory.SubFactory(YearFactory)
    employee_id = factory.LazyAttribute(lambda o: o.employee_obj.id)
    year_id = factory.LazyAttribute(lambda o: o.year_obj.id)


class GradeSectionLinkFactory(TypedFactory[GradeSectionLink]):
    class Meta:
        model = GradeSectionLink
        exclude = ("grade_obj", "section_obj")

    grade_obj = factory.SubFactory(GradeFactory)
    section_obj = factory.SubFactory(
        SectionFactory, grade_obj=factory.SelfAttribute("..grade_obj")
    )
    grade_id = factory.LazyAttribute(lambda o: o.grade_obj.id)
    section_id = factory.LazyAttribute(lambda o: o.section_obj.id)


class GradeStreamLinkFactory(TypedFactory[GradeStreamLink]):
    class Meta:
        model = GradeStreamLink
        exclude = ("grade_obj", "stream_obj")

    grade_obj = factory.SubFactory(GradeFactory, has_stream=True)
    stream_obj = factory.SubFactory(
        StreamFactory, grade_obj=factory.SelfAttribute("..grade_obj")
    )
    grade_id = factory.LazyAttribute(lambda o: o.grade_obj.id)
    stream_id = factory.LazyAttribute(lambda o: o.stream_obj.id)


class StudentYearRecordFactory(TypedFactory[StudentYearRecord]):
    class Meta:
        model = StudentYearRecord
        exclude = ("student_obj", "grade_obj", "year_obj", "stream_obj")

    student_obj = factory.SubFactory(StudentFactory)
    grade_obj = factory.SubFactory(GradeFactory)
    year_obj = factory.SubFactory(YearFactory)
    stream_obj = factory.SubFactory(
        StreamFactory, grade_obj=factory.SelfAttribute("..grade_obj")
    )

    student_id = factory.LazyAttribute(lambda o: o.student_obj.id)
    grade_id = factory.LazyAttribute(lambda o: o.grade_obj.id)
    year_id = factory.LazyAttribute(lambda o: o.year_obj.id)
    stream_id = factory.LazyAttribute(
        lambda o: o.stream_obj.id if o.stream_obj else None
    )
    final_score = factory.LazyFunction(lambda: round(random.uniform(50, 100), 2))
    rank = factory.LazyFunction(lambda: random.randint(1, 50))

    class Params:
        no_stream = factory.Trait(stream_obj=None, stream_id=None)


class TeacherRecordLinkFactory(TypedFactory[TeacherRecordLink]):
    class Meta:
        model = TeacherRecordLink
        exclude = ("teacher_record_obj", "section_obj")

    teacher_record_obj = factory.SubFactory(TeacherRecordFactory)
    section_obj = factory.SubFactory(
        SectionFactory,
    )
    teacher_record_id = factory.LazyAttribute(lambda o: o.teacher_record_obj.id)
    section_id = factory.LazyAttribute(lambda o: o.section_obj.id)
