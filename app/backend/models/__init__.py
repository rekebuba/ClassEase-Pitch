#!/usr/bin/python3
"""This module initializes the storage system for ClassEase"""

from models.academic_term import AcademicTerm
from models.admin import Admin
from models.assessment import Assessment
from models.blacklist_token import BlacklistToken
from models.employee import Employee
from models.employee_year_link import EmployeeYearLink
from models.event import Event
from models.grade import Grade
from models.grade_section_link import GradeSectionLink
from models.grade_stream_link import GradeStreamLink
from models.grade_stream_subject import GradeStreamSubject
from models.mark_list import MarkList
from models.registration import Registration
from models.saved_query_view import SavedQueryView
from models.section import Section
from models.stream import Stream
from models.student import Student
from models.student_academic_term_link import StudentAcademicTermLink
from models.student_grade_link import StudentGradeLink
from models.student_section_link import StudentSectionLink
from models.student_stream_link import StudentStreamLink
from models.student_subject_link import StudentSubjectLink
from models.student_term_record import StudentTermRecord
from models.student_year_link import StudentYearLink
from models.student_year_record import StudentYearRecord
from models.subject import Subject
from models.subject_yearly_average import SubjectYearlyAverage
from models.table import Table
from models.teacher_record import TeacherRecord
from models.teacher_record_link import TeacherRecordLink
from models.user import User
from models.year import Year
from models.yearly_subject import YearlySubject

__all__ = [
    "AcademicTerm",
    "Admin",
    "Assessment",
    "BlacklistToken",
    "Event",
    "Grade",
    "GradeSectionLink",
    "GradeStreamLink",
    "GradeStreamSubject",
    "MarkList",
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
    "Employee",
    "TeacherRecordLink",
    "TeacherRecord",
    "User",
    "Year",
    "YearlySubject",
    "EmployeeYearLink",
]
