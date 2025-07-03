"""
This package contains the factories for creating test data.
"""

from .default_felids import DefaultFelids
from .base_factory import BaseFactory
from .typed_factory import TypedFactory
from .year_factory import YearFactory
from .grade_factory import GradeFactory
from .event_factory import EventFactory
from .academic_term_factory import AcademicTermFactory
from .user_factory import UserFactory
from .admin_factory import AdminFactory
from .student_factory import StudentFactory
from .teacher_factory import TeacherFactory
from .subject_factory import SubjectFactory
from .section_factory import SectionFactory
from .student_term_record_factory import StudentTermRecordFactory
from .student_year_record_factory import StudentYearRecordFactory
from .assessment_factory import AssessmentFactory
from .subjects_factory import SubjectsFactory, AvailableSubject
from .assessment_types_factory import AssessmentTypesFactory, AssessmentTypes
from .mark_assessment_factory import MarkAssessmentFactory, MarkAssessment
from .mark_list_factory import MarkListFactory, FakeMarkList
from .sort_query_factory import SortQueryFactory, SortQuery
from .variant_factory import variantFactory, Variant
from .table_id_factory import TableIdFactory, Value
from .min_max_factory import MinMaxFactory, MinMax
from .value_factory import valueFactory
from .filter_query_factory import FilterQueryFactory, FilterQuery
from .search_params_factory import SearchParamsFactory, SearchParams
from .query_factory import QueryFactory, QueryResponse
from .yearly_subject_factory import YearlySubjectFactory
from .stream_factory import StreamFactory

__all__ = [
    "DefaultFelids",
    "BaseFactory",
    "TypedFactory",
    "YearFactory",
    "GradeFactory",
    "EventFactory",
    "AcademicTermFactory",
    "UserFactory",
    "AdminFactory",
    "StudentFactory",
    "TeacherFactory",
    "SubjectFactory",
    "SectionFactory",
    "StudentTermRecordFactory",
    "StudentYearRecordFactory",
    "AssessmentFactory",
    "SubjectsFactory",
    "AvailableSubject",
    "AssessmentTypesFactory",
    "AssessmentTypes",
    "MarkAssessmentFactory",
    "MarkAssessment",
    "MarkListFactory",
    "FakeMarkList",
    "SortQueryFactory",
    "SortQuery",
    "variantFactory",
    "Variant",
    "TableIdFactory",
    "Value",
    "MinMaxFactory",
    "MinMax",
    "valueFactory",
    "FilterQueryFactory",
    "FilterQuery",
    "SearchParamsFactory",
    "SearchParams",
    "QueryFactory",
    "QueryResponse",
    "YearlySubjectFactory",
    "StreamFactory",
]
