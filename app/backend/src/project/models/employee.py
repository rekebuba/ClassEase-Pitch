import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    UUID,
    CheckConstraint,
    Date,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.models.grade import Grade
from project.models.teacher_record import TeacherRecord
from project.utils.enum import (
    EmployeeApplicationStatusEnum,
    EmployeePositionEnum,
    ExperienceYearEnum,
    GenderEnum,
    HighestEducationEnum,
    MaritalStatusEnum,
)
from project.utils.utils import sort_grade_key

if TYPE_CHECKING:
    from project.models.subject import Subject
    from project.models.user import User
    from project.models.year import Year


class Employee(BaseModel):
    """
    This model represents an employee in the ClassEase system.
    It inherits from BaseModel and Base.
    """

    __tablename__ = "employees"

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    father_name: Mapped[str] = mapped_column(String(50), nullable=False)
    grand_father_name: Mapped[str] = mapped_column(String(50), nullable=False)
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    gender: Mapped[GenderEnum] = mapped_column(
        Enum(
            GenderEnum,
            name="gender_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )
    nationality: Mapped[str] = mapped_column(String(50), nullable=False)
    social_security_number: Mapped[str] = mapped_column(String(50), nullable=False)

    # Contact Information
    address: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    primary_phone: Mapped[str] = mapped_column(String(50), nullable=False)
    personal_email: Mapped[str] = mapped_column(String(50), nullable=False)

    # Emergency Contact
    emergency_contact_name: Mapped[str] = mapped_column(String(50), nullable=False)
    emergency_contact_relation: Mapped[str] = mapped_column(String(50), nullable=False)
    emergency_contact_phone: Mapped[str] = mapped_column(String(50), nullable=False)

    # Educational Background
    highest_education: Mapped[HighestEducationEnum] = mapped_column(
        Enum(
            HighestEducationEnum,
            name="highest_education_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
    )
    university: Mapped[str] = mapped_column(String(50), nullable=False)
    graduation_year: Mapped[int] = mapped_column(Integer, nullable=False)
    gpa: Mapped[float] = mapped_column(Float, nullable=False)

    position: Mapped[EmployeePositionEnum] = mapped_column(
        Enum(
            EmployeePositionEnum,
            name="employee_position_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
    )
    years_of_experience: Mapped[ExperienceYearEnum] = mapped_column(
        Enum(
            ExperienceYearEnum,
            name="experience_year_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )

    # Background & References
    reference1_name: Mapped[str] = mapped_column(String(50), nullable=False)
    reference1_organization: Mapped[str] = mapped_column(String(50), nullable=False)
    reference1_phone: Mapped[str] = mapped_column(String(50), nullable=False)

    # Additional Information (Default values)
    reference1_email: Mapped[Optional[str]] = mapped_column(String(50), default=None)
    marital_status: Mapped[Optional[MaritalStatusEnum]] = mapped_column(
        Enum(
            MaritalStatusEnum,
            name="marital_status_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=True,
        default=None,
    )

    secondary_phone: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )

    certifications: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, default=None
    )

    resume: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    background_check: Mapped[Optional[str]] = mapped_column(Text, default=None)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=True,
        default=None,
    )
    subject_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(),
        ForeignKey("subjects.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )  # For Teaching positions
    major_subject: AssociationProxy[Optional["Subject"]] = association_proxy(
        "subject",
        "name",
        default=None,
    )
    status: Mapped[EmployeeApplicationStatusEnum] = mapped_column(
        Enum(
            EmployeeApplicationStatusEnum,
            name="status_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=EmployeeApplicationStatusEnum.PENDING,
    )

    @hybrid_property
    def full_name(self):
        return self.first_name + " " + self.father_name + " " + self.grand_father_name

    @full_name.expression  # type: ignore
    def full_name(cls):
        return cls.first_name + " " + cls.father_name + " " + cls.grand_father_name

    # Relationship with Default
    user: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="employee",
        init=False,
        repr=False,
        passive_deletes=True,
    )

    years: Mapped[List["Year"]] = relationship(
        "Year",
        secondary="employee_year_links",
        back_populates="employees",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    # One-To-Many Relationships
    teacher_records: Mapped[List["TeacherRecord"]] = relationship(
        "TeacherRecord",
        back_populates="employee",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    subject: Mapped[Optional["Subject"]] = relationship(
        "Subject",
        back_populates="teachers",
        init=False,
        repr=False,
        passive_deletes=True,
    )

    _subjects: AssociationProxy[List["Subject"]] = association_proxy(
        "teacher_records",
        "subject",
        default_factory=list,
    )

    @property
    def subjects(self) -> List["Subject"]:
        """Return unique, non-null subjects."""
        seen = set()
        result = []
        for s in self._subjects:
            if s is not None and s.id not in seen and s.id != self.subject_id:
                seen.add(s.id)
                result.append(s)

        return sorted(result, key=lambda x: x.name)

    _grades: AssociationProxy[List["Grade"]] = association_proxy(
        "teacher_records",
        "grade",
        default_factory=list,
    )

    @property
    def grades(self) -> List["Grade"]:
        """Return unique grades that have streams assigned to this subject."""
        seen = set()
        result = []
        for g in self._grades:
            if g is not None and g.id not in seen:
                seen.add(g.id)
                result.append(g)
        return sorted(result, key=sort_grade_key)

    __table_args__ = (
        CheckConstraint("gpa >= 0.0 AND gpa <= 4.0", name="check_employee_gpa_range"),
    )
