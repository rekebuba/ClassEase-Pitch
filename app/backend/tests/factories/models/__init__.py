"""
This package contains the factories for creating test data.
"""

from .default_felids import DefaultFelids
from .base_factory import BaseFactory
from .year_factory import YearFactory
from .grade_factory import GradeFactory
from .event_factory import EventFactory
from .academic_term_factory import AcademicTermFactory
from .user_factory import UserFactory
from .admin_factory import AdminFactory
from .student_factory import StudentFactory
from .teacher_factory import TeacherFactory
from .teacher_record_factory import TeacherRecordFactory
from .subject_factory import SubjectFactory
from .section_factory import SectionFactory
from .student_term_record_factory import StudentTermRecordFactory
from .student_year_record_factory import StudentYearRecordFactory
from .assessment_factory import AssessmentFactory
from .subjects_factory import SubjectsFactory, AvailableSubject
from .assessment_types_factory import AssessmentTypesFactory, AssessmentTypes
from .mark_assessment_factory import MarkAssessmentFactory, MarkAssessment
from .mark_list_factory import MarkListFactory
from ..api.sort_query_factory import SortQueryFactory, SortQuery
from ..api.variant_factory import variantFactory, Variant
from ..api.table_id_factory import TableIdFactory, Value
from ..api.min_max_factory import MinMaxFactory, MinMax
from ..api.value_factory import valueFactory
from ..api.filter_query_factory import FilterQueryFactory, FilterQuery
from ..api.search_params_factory import SearchParamsFactory, SearchParams
from ..api.query_factory import QueryFactory, QueryResponse
from .yearly_subject_factory import YearlySubjectFactory
from .stream_factory import StreamFactory
from .student_year_link_factory import StudentYearLinkFactory

__all__ = [
    "DefaultFelids",
    "BaseFactory",
    "YearFactory",
    "GradeFactory",
    "EventFactory",
    "AcademicTermFactory",
    "UserFactory",
    "AdminFactory",
    "StudentFactory",
    "TeacherFactory",
    "TeacherRecordFactory",
    "SubjectFactory",
    "SectionFactory",
    "StudentTermRecordFactory",
    "StudentYearRecordFactory",
    "StudentYearLinkFactory",
    "AssessmentFactory",
    "SubjectsFactory",
    "AvailableSubject",
    "AssessmentTypesFactory",
    "AssessmentTypes",
    "MarkAssessmentFactory",
    "MarkAssessment",
    "MarkListFactory",
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
