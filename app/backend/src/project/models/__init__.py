#!/usr/bin/python3
"""This module initializes the storage system for ClassEase"""

from project.models.academic_term import AcademicTerm
from project.models.admin import Admin
from project.models.assessment import Assessment
from project.models.blacklist_token import BlacklistToken
from project.models.employee import Employee
from project.models.employee_year_link import EmployeeYearLink
from project.models.event import Event
from project.models.grade import Grade
from project.models.grade_section_link import GradeSectionLink
from project.models.grade_stream_link import GradeStreamLink
from project.models.grade_stream_subject import GradeStreamSubject
from project.models.mark_list import MarkList
from project.models.parent import Parent
from project.models.parent_student_link import ParentStudentLink
from project.models.registration import Registration
from project.models.saved_query_view import SavedQueryView
from project.models.section import Section
from project.models.stream import Stream
from project.models.student import Student
from project.models.student_academic_term_link import StudentAcademicTermLink
from project.models.student_grade_link import StudentGradeLink
from project.models.student_section_link import StudentSectionLink
from project.models.student_stream_link import StudentStreamLink
from project.models.student_subject_link import StudentSubjectLink
from project.models.student_term_record import StudentTermRecord
from project.models.student_year_link import StudentYearLink
from project.models.student_year_record import StudentYearRecord
from project.models.subject import Subject
from project.models.subject_yearly_average import SubjectYearlyAverage
from project.models.table import Table
from project.models.teacher_record import TeacherRecord
from project.models.teacher_record_link import TeacherRecordLink
from project.models.user import User
from project.models.year import Year
from project.models.yearly_subject import YearlySubject

__all__ = [
    "AcademicTerm",
    "Admin",
    "Assessment",
    "BlacklistToken",
    "Employee",
    "EmployeeYearLink",
    "Event",
    "Grade",
    "GradeSectionLink",
    "GradeStreamLink",
    "GradeStreamSubject",
    "MarkList",
    "Parent",
    "ParentStudentLink",
    "Registration",
    "SavedQueryView",
    "Section",
    "Stream",
    "Student",
    "StudentAcademicTermLink",
    "StudentGradeLink",
    "StudentSectionLink",
    "StudentStreamLink",
    "StudentSubjectLink",
    "StudentTermRecord",
    "StudentYearLink",
    "StudentYearRecord",
    "Subject",
    "SubjectYearlyAverage",
    "Table",
    "TeacherRecord",
    "TeacherRecordLink",
    "User",
    "Year",
    "YearlySubject",
]
