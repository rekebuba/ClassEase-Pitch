#!/usr/bin/python3
"""This module initializes the storage system for ClassEase"""

from models.engine.db_storage import DBStorage

storage = DBStorage()

from models.academic_term import AcademicTerm
from models.admin import Admin
from models.assessment import Assessment
from models.blacklist_token import BlacklistToken
from models.ceo import CEO
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
from models.teacher import Teacher
from models.teacher_academic_term_link import TeacherAcademicTermLink
from models.teacher_grade_link import TeacherGradeLink
from models.teacher_section_link import TeacherSectionLink
from models.teacher_subject_link import TeacherSubjectLink
from models.teacher_term_record import TeacherTermRecord
from models.teacher_year_link import TeacherYearLink
from models.user import User
from models.year import Year
from models.yearly_subject import YearlySubject
