import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    CheckConstraint,
    Date,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base.base_model import BaseModel
from models.base.column_type import UUIDType
from models.teacher_record import TeacherRecord
from utils.enum import (
    EmployeeApplicationStatus,
    EmployeePositionEnum,
    ExperienceYearEnum,
    GenderEnum,
    HighestEducationEnum,
    MaritalStatusEnum,
)

if TYPE_CHECKING:
    from models.user import User


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
        UUIDType(),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=True,
        default=None,
    )
    status: Mapped[EmployeeApplicationStatus] = mapped_column(
        Enum(
            EmployeeApplicationStatus,
            name="status_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=EmployeeApplicationStatus.PENDING,
    )

    # Relationship with Default
    user: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="employee",
        init=False,
        repr=False,
        passive_deletes=True,
    )

    # One-To-Many Relationships
    teacher_records: Mapped[List["TeacherRecord"]] = relationship(
        "TeacherRecord",
        back_populates="teacher",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )

    __table_args__ = (
        CheckConstraint("gpa >= 0.0 AND gpa <= 4.0", name="check_employee_gpa_range"),
    )
