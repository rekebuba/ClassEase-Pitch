from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlalchemy import JSON, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.models.base.base_model import BaseModel
from project.utils.enum import SchoolStatusEnum

if TYPE_CHECKING:
    from project.models.audit_log import AuditLog
    from project.models.class_section import ClassSection
    from project.models.department import Department
    from project.models.employee import Employee
    from project.models.employee_position import EmployeePosition
    from project.models.employment_application import EmploymentApplication
    from project.models.employment_contract import EmploymentContract
    from project.models.employment_position import EmploymentPosition
    from project.models.enrollment_application import EnrollmentApplication
    from project.models.enrollment_opportunity import EnrollmentOpportunity
    from project.models.payroll_entry import PayrollEntry
    from project.models.payroll_profile import PayrollProfile
    from project.models.payroll_run import PayrollRun
    from project.models.position import Position
    from project.models.school_membership import SchoolMembership
    from project.models.stream import Stream
    from project.models.student import Student
    from project.models.subject_offering import SubjectOffering
    from project.models.teacher_profile import TeacherProfile
    from project.models.teacher_subject import TeacherSubject
    from project.models.teaching_assignment import TeachingAssignment
    from project.models.transfer_request import TransferRequest
    from project.models.year import Year


class School(BaseModel):
    __tablename__ = "schools"

    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    status: Mapped[SchoolStatusEnum] = mapped_column(
        Enum(
            SchoolStatusEnum,
            name="school_status_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
        default=SchoolStatusEnum.ACTIVE,
    )
    domain: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, default=None)
    logo_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, default=None)
    primary_color: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, default=None)
    settings: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
        default_factory=dict,
    )

    memberships: Mapped[List["SchoolMembership"]] = relationship(
        "SchoolMembership",
        back_populates="school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    years: Mapped[List["Year"]] = relationship(
        "Year",
        back_populates="school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    employees: Mapped[List["Employee"]] = relationship(
        "Employee",
        back_populates="school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="membership",
    )
    departments: Mapped[List["Department"]] = relationship(
        "Department",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="school",
    )
    positions: Mapped[List["Position"]] = relationship(
        "Position",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="school",
    )
    employment_positions: Mapped[List["EmploymentPosition"]] = relationship(
        "EmploymentPosition",
        back_populates="school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    employment_applications: Mapped[List["EmploymentApplication"]] = relationship(
        "EmploymentApplication",
        back_populates="school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    enrollment_opportunities: Mapped[List["EnrollmentOpportunity"]] = relationship(
        "EnrollmentOpportunity",
        back_populates="school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    enrollment_applications: Mapped[List["EnrollmentApplication"]] = relationship(
        "EnrollmentApplication",
        back_populates="school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    employee_positions: Mapped[List["EmployeePosition"]] = relationship(
        "EmployeePosition",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="employee,employee_positions,position,school",
    )
    teacher_profiles: Mapped[List["TeacherProfile"]] = relationship(
        "TeacherProfile",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="teacher_profile",
    )
    streams: Mapped[List["Stream"]] = relationship(
        "Stream",
        back_populates="school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="school,grade,stream,streams,subject,subject_offerings,year",
    )
    class_sections: Mapped[List["ClassSection"]] = relationship(
        "ClassSection",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="academic_year,class_sections,grade_stream,homeroom_teacher,school,section",
    )
    subject_offerings: Mapped[List["SubjectOffering"]] = relationship(
        "SubjectOffering",
        back_populates="school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="school,grade,stream,subject,subject_offerings,year",
    )
    teacher_subjects: Mapped[List["TeacherSubject"]] = relationship(
        "TeacherSubject",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    teaching_assignments: Mapped[List["TeachingAssignment"]] = relationship(
        "TeachingAssignment",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="teaching_assignments",
    )
    payroll_profiles: Mapped[List["PayrollProfile"]] = relationship(
        "PayrollProfile",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="employee,payroll_profile,school",
    )
    payroll_runs: Mapped[List["PayrollRun"]] = relationship(
        "PayrollRun",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="school",
    )
    payroll_entries: Mapped[List["PayrollEntry"]] = relationship(
        "PayrollEntry",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="employee,payroll_entries,payroll_run,school",
    )
    employment_contracts: Mapped[List["EmploymentContract"]] = relationship(
        "EmploymentContract",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="employee,employment_contracts,school",
    )
    students: Mapped[List["Student"]] = relationship(
        "Student",
        back_populates="school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    audit_logs: Mapped[List["AuditLog"]] = relationship(
        "AuditLog",
        back_populates="school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
        overlaps="audit_logs,auth_session,membership",
    )
    initiated_transfers: Mapped[List["TransferRequest"]] = relationship(
        "TransferRequest",
        foreign_keys="TransferRequest.source_school_id",
        back_populates="source_school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
    received_transfers: Mapped[List["TransferRequest"]] = relationship(
        "TransferRequest",
        foreign_keys="TransferRequest.target_school_id",
        back_populates="target_school",
        default_factory=list,
        repr=False,
        passive_deletes=True,
    )
