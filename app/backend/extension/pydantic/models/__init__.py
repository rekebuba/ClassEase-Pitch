from .teacher_term_record_schema import (
    TeacherTermRecordRelatedSchema,
    TeacherTermRecordSchema,
    TeacherTermRecordWithRelatedSchema,
)
from .academic_term_schema import (
    AcademicTermRelatedSchema,
    AcademicTermSchema,
    AcademicTermWithRelatedSchema,
)
from .admin_schema import (
    AdminRelatedSchema,
    AdminSchema,
    AdminWithRelatedSchema,
)
from .assessment_schema import (
    AssessmentRelatedSchema,
    AssessmentSchema,
)
from .blacklist_token_schema import BlacklistTokenSchema
from .event_schema import EventRelatedSchema, EventSchema, EventWithRelatedSchema
from .grade_schema import (
    GradeNestedSchema,
    GradeRelatedSchema,
    GradeSchema,
    GradeWithRelatedSchema,
)
from .grade_stream_link_schema import GradeStreamLinkSchema
from .mark_list_schema import MarkListSchema
from .registration_schema import RegistrationSchema
from .saved_query_view_schema import (
    SavedQueryViewRelatedSchema,
    SavedQueryViewSchema,
)
from .section_schema import (
    SectionRelatedSchema,
    SectionSchema,
    SectionWithRelatedSchema,
)
from .stream_schema import (
    StreamRelatedSchema,
    StreamSchema,
    StreamWithRelatedSchema,
)
from .student_schema import (
    StudentRelatedSchema,
    StudentSchema,
    StudentWithRelatedSchema,
)
from .student_term_record_schema import (
    StudentTermRecordRelatedSchema,
    StudentTermRecordSchema,
    StudentTermRecordWithRelatedSchema,
)
from .student_year_record_schema import (
    StudentYearRecordRelatedSchema,
    StudentYearRecordSchema,
    StudentYearRecordWithRelatedSchema,
)
from .subject_schema import (
    SubjectNestedSchema,
    SubjectRelatedSchema,
    SubjectSchema,
    SubjectWithRelatedSchema,
)
from .subject_yearly_average_schema import (
    SubjectYearlyAverageRelatedSchema,
    SubjectYearlyAverageSchema,
)
from .table_schema import TableSchema
from .teacher_grade_link_schema import TeacherGradeLinkSchema
from .teacher_record_schema import (
    TeacherRecordRelatedSchema,
    TeacherRecordSchema,
)
from .teacher_schema import (
    TeacherRelatedSchema,
    TeacherSchema,
    TeacherWithRelatedSchema,
)
from .teacher_subject_link_schema import TeacherSubjectLinkSchema
from .user_schema import UserRelatedSchema, UserSchema, UserWithRelatedSchema
from .year_schema import (
    YearNestedSchema,
    YearRelatedSchema,
    YearSchema,
    YearWithRelatedSchema,
)
from .yearly_subject_schema import (
    YearlySubjectRelatedSchema,
    YearlySubjectSchema,
)

__all__ = [
    "AcademicTermSchema",
    "AcademicTermRelatedSchema",
    "AcademicTermWithRelatedSchema",
    "AdminSchema",
    "AdminRelatedSchema",
    "AdminWithRelatedSchema",
    "AssessmentSchema",
    "AssessmentRelatedSchema",
    "BlacklistTokenSchema",
    "EventSchema",
    "EventRelatedSchema",
    "EventWithRelatedSchema",
    "GradeSchema",
    "GradeRelatedSchema",
    "GradeNestedSchema",
    "GradeWithRelatedSchema",
    "GradeStreamLinkSchema",
    "MarkListSchema",
    "RegistrationSchema",
    "SavedQueryViewSchema",
    "SavedQueryViewRelatedSchema",
    "SectionSchema",
    "SectionRelatedSchema",
    "SectionWithRelatedSchema",
    "StreamSchema",
    "StreamRelatedSchema",
    "StudentSchema",
    "StudentWithRelatedSchema",
    "StudentRelatedSchema",
    "StudentTermRecordSchema",
    "StudentTermRecordRelatedSchema",
    "StudentTermRecordWithRelatedSchema",
    "StudentYearRecordSchema",
    "StudentYearRecordRelatedSchema",
    "StudentYearRecordWithRelatedSchema",
    "SubjectSchema",
    "SubjectRelatedSchema",
    "SubjectNestedSchema",
    "SubjectWithRelatedSchema",
    "SubjectYearlyAverageSchema",
    "SubjectYearlyAverageRelatedSchema",
    "TableSchema",
    "TeacherGradeLinkSchema",
    "TeacherRecordSchema",
    "TeacherRecordRelatedSchema",
    "TeacherSchema",
    "TeacherRelatedSchema",
    "TeacherWithRelatedSchema",
    "TeacherSubjectLinkSchema",
    "UserSchema",
    "UserRelatedSchema",
    "UserWithRelatedSchema",
    "YearSchema",
    "YearRelatedSchema",
    "YearNestedSchema",
    "YearWithRelatedSchema",
    "YearlySubjectSchema",
    "YearlySubjectRelatedSchema",
]

AcademicTermSchema.model_rebuild()
AcademicTermRelatedSchema.model_rebuild()
AcademicTermWithRelatedSchema.model_rebuild()
AdminSchema.model_rebuild()
AdminRelatedSchema.model_rebuild()
AdminWithRelatedSchema.model_rebuild()
AssessmentSchema.model_rebuild()
AssessmentRelatedSchema.model_rebuild()

EventSchema.model_rebuild()
EventRelatedSchema.model_rebuild()
EventWithRelatedSchema.model_rebuild()

GradeSchema.model_rebuild()
GradeRelatedSchema.model_rebuild()
GradeNestedSchema.model_rebuild()
GradeWithRelatedSchema.model_rebuild()

MarkListSchema.model_rebuild()
SavedQueryViewSchema.model_rebuild()
SavedQueryViewRelatedSchema.model_rebuild()
SectionSchema.model_rebuild()
SectionRelatedSchema.model_rebuild()
SectionWithRelatedSchema.model_rebuild()
StreamSchema.model_rebuild()
StreamRelatedSchema.model_rebuild()
StreamWithRelatedSchema.model_rebuild()
StudentSchema.model_rebuild()
StudentWithRelatedSchema.model_rebuild()
StudentRelatedSchema.model_rebuild()
StudentTermRecordSchema.model_rebuild()
StudentTermRecordRelatedSchema.model_rebuild()
StudentTermRecordWithRelatedSchema.model_rebuild()

StudentYearRecordSchema.model_rebuild()
StudentYearRecordRelatedSchema.model_rebuild()
StudentYearRecordWithRelatedSchema.model_rebuild()

SubjectSchema.model_rebuild()
SubjectRelatedSchema.model_rebuild()
SubjectNestedSchema.model_rebuild()
SubjectWithRelatedSchema.model_rebuild()
SubjectYearlyAverageSchema.model_rebuild()
SubjectYearlyAverageRelatedSchema.model_rebuild()
TeacherRecordSchema.model_rebuild()
TeacherRecordRelatedSchema.model_rebuild()
TeacherSchema.model_rebuild()
TeacherRelatedSchema.model_rebuild()
TeacherWithRelatedSchema.model_rebuild()
TeacherTermRecordSchema.model_rebuild()
TeacherTermRecordRelatedSchema.model_rebuild()
TeacherTermRecordWithRelatedSchema.model_rebuild()
UserSchema.model_rebuild()
UserRelatedSchema.model_rebuild()
UserWithRelatedSchema.model_rebuild()

YearSchema.model_rebuild()
YearRelatedSchema.model_rebuild()
YearNestedSchema.model_rebuild()
YearWithRelatedSchema.model_rebuild()

YearlySubjectSchema.model_rebuild()
YearlySubjectRelatedSchema.model_rebuild()
