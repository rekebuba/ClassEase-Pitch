#!/usr/bin/python3
"""This module initializes the storage system for ClassEase"""

from project.models.academic_term import AcademicTerm
from project.models.assessment import Assessment
from project.models.assessment_scheme import AssessmentScheme
from project.models.assessment_scheme_component import AssessmentSchemeComponent
from project.models.audit_log import AuditLog
from project.models.auth_identity import AuthIdentity
from project.models.auth_session import AuthSession
from project.models.blacklist_token import BlacklistToken
from project.models.class_section import ClassSection
from project.models.department import Department
from project.models.employee import Employee
from project.models.employee_position import EmployeePosition
from project.models.employment_contract import EmploymentContract
from project.models.event import Event
from project.models.grade import Grade
from project.models.grade_stream import GradeStream
from project.models.employment_application import EmploymentApplication
from project.models.employment_position import EmploymentPosition
from project.models.employment_profile import EmploymentProfile
from project.models.enrollment_application import EnrollmentApplication
from project.models.enrollment_opportunity import EnrollmentOpportunity
from project.models.membership_role import MembershipRole
from project.models.parent import Parent
from project.models.parent_student_link import ParentStudentLink
from project.models.payroll_entry import PayrollEntry
from project.models.payroll_profile import PayrollProfile
from project.models.payroll_run import PayrollRun
from project.models.permission import Permission
from project.models.position import Position
from project.models.role import Role
from project.models.role_permission import RolePermission
from project.models.saved_query_view import SavedQueryView
from project.models.school import School
from project.models.school_membership import SchoolMembership
from project.models.section import Section
from project.models.stream import Stream
from project.models.student import Student
from project.models.student_enrollments import StudentEnrollment
from project.models.student_term_record import StudentTermRecord
from project.models.student_year_record import StudentYearRecord
from project.models.subject import Subject
from project.models.subject_offering import SubjectOffering
from project.models.subject_term_result import SubjectTermResult
from project.models.subject_yearly_average import SubjectYearlyAverage
from project.models.table import Table
from project.models.teacher_profile import TeacherProfile
from project.models.teacher_subject import TeacherSubject
from project.models.teaching_assignment import TeachingAssignment
from project.models.transfer_request import TransferRequest
from project.models.user import User
from project.models.year import Year

__all__ = [
    "AcademicTerm",
    "Assessment",
    "AssessmentScheme",
    "AssessmentSchemeComponent",
    "AuditLog",
    "AuthIdentity",
    "AuthSession",
    "BlacklistToken",
    "ClassSection",
    "Department",
    "Employee",
    "EmployeePosition",
    "EmployeeYearLink",
    "EmploymentContract",
    "Event",
    "Grade",
    "GradeStream",
    "EmploymentApplication",
    "EmploymentPosition",
    "EmploymentProfile",
    "EnrollmentApplication",
    "EnrollmentOpportunity",
    "MembershipRole",
    "Parent",
    "ParentStudentLink",
    "PayrollEntry",
    "PayrollProfile",
    "PayrollRun",
    "Permission",
    "Position",
    "Role",
    "RolePermission",
    "SavedQueryView",
    "School",
    "SchoolMembership",
    "Section",
    "Stream",
    "Student",
    "StudentEnrollment",
    "StudentTermRecord",
    "StudentYearRecord",
    "StudentYearRecord",
    "Subject",
    "SubjectOffering",
    "SubjectOffering",
    "SubjectTermResult",
    "SubjectYearlyAverage",
    "Table",
    "TeacherProfile",
    "TeacherSubject",
    "TeachingAssignment",
    "TransferRequest",
    "User",
    "Year",
]
