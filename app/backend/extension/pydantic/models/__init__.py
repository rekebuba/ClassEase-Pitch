from .academic_term_schema import (
    AcademicTermRelationshipSchema,
    AcademicTermSchema,
    AcademicTermSchemaWithRelationships,
)
from .admin_schema import (
    AdminRelationshipSchema,
    AdminSchema,
    AdminWithRelationshipsSchema,
)
from .assessment_schema import (
    AssessmentRelationshipSchema,
    AssessmentSchema,
)
from .blacklist_token_schema import BlacklistTokenSchema
from .event_schema import EventRelationshipSchema, EventSchema
from .grade_schema import (
    GradeRelationshipSchema,
    GradeSchema,
    GradeWithRelationshipsSchema,
)
from .grade_stream_link_schema import GradeStreamLinkSchema
from .mark_list_schema import MarkListSchema
from .registration_schema import RegistrationSchema
from .saved_query_view_schema import (
    SavedQueryViewRelationshipSchema,
    SavedQueryViewSchema,
)
from .section_schema import (
    SectionRelationshipSchema,
    SectionSchema,
    SectionSchemaWithRelationships,
)
from .stream_schema import StreamRelationshipSchema, StreamSchema
from .student_schema import (
    StudentRelationshipSchema,
    StudentSchema,
    StudentWithRelationshipsSchema,
)
from .student_term_record_schema import (
    StudentTermRecordRelationshipSchema,
    StudentTermRecordSchema,
)
from .student_year_record_schema import (
    StudentYearRecordRelationshipSchema,
    StudentYearRecordSchema,
)
from .subject_schema import (
    SubjectRelationshipSchema,
    SubjectSchema,
    SubjectWithRelationshipsSchema,
)
from .subject_yearly_average_schema import (
    SubjectYearlyAverageRelationshipSchema,
    SubjectYearlyAverageSchema,
)
from .table_schema import TableSchema
from .teacher_grade_link_schema import TeacherGradeLinkSchema
from .teacher_record_schema import (
    TeacherRecordRelationshipSchema,
    TeacherRecordSchema,
)
from .teacher_schema import (
    TeacherRelationshipSchema,
    TeacherSchema,
    TeacherWithRelationshipsSchema,
)
from .teacher_subject_link_schema import TeacherSubjectLinkSchema
from .user_schema import UserRelationshipSchema, UserSchema, UserWithRelationshipsSchema
from .year_schema import YearRelationshipSchema, YearSchema, YearSchemaWithRelationships
from .yearly_subject_schema import (
    YearlySubjectRelationshipSchema,
    YearlySubjectSchema,
)

__all__ = [
    "AcademicTermSchema",
    "AcademicTermRelationshipSchema",
    "AcademicTermSchemaWithRelationships",
    "AdminSchema",
    "AdminRelationshipSchema",
    "AdminWithRelationshipsSchema",
    "AssessmentSchema",
    "AssessmentRelationshipSchema",
    "BlacklistTokenSchema",
    "EventSchema",
    "EventRelationshipSchema",
    "GradeSchema",
    "GradeRelationshipSchema",
    "GradeWithRelationshipsSchema",
    "GradeStreamLinkSchema",
    "MarkListSchema",
    "RegistrationSchema",
    "SavedQueryViewSchema",
    "SavedQueryViewRelationshipSchema",
    "SectionSchema",
    "SectionRelationshipSchema",
    "SectionSchemaWithRelationships",
    "StreamSchema",
    "StreamRelationshipSchema",
    "StudentSchema",
    "StudentWithRelationshipsSchema",
    "StudentRelationshipSchema",
    "StudentTermRecordSchema",
    "StudentTermRecordRelationshipSchema",
    "StudentYearRecordSchema",
    "StudentYearRecordRelationshipSchema",
    "SubjectSchema",
    "SubjectRelationshipSchema",
    "SubjectWithRelationshipsSchema",
    "SubjectYearlyAverageSchema",
    "SubjectYearlyAverageRelationshipSchema",
    "TableSchema",
    "TeacherGradeLinkSchema",
    "TeacherRecordSchema",
    "TeacherRecordRelationshipSchema",
    "TeacherSchema",
    "TeacherRelationshipSchema",
    "TeacherWithRelationshipsSchema",
    "TeacherSubjectLinkSchema",
    "UserSchema",
    "UserRelationshipSchema",
    "UserWithRelationshipsSchema",
    "YearSchema",
    "YearRelationshipSchema",
    "YearSchemaWithRelationships",
    "YearlySubjectSchema",
    "YearlySubjectRelationshipSchema",
]

AcademicTermSchema.model_rebuild()
AcademicTermRelationshipSchema.model_rebuild()
AcademicTermSchemaWithRelationships.model_rebuild()
AdminSchema.model_rebuild()
AdminRelationshipSchema.model_rebuild()
AdminWithRelationshipsSchema.model_rebuild()
AssessmentSchema.model_rebuild()
AssessmentRelationshipSchema.model_rebuild()
EventSchema.model_rebuild()
EventRelationshipSchema.model_rebuild()
GradeSchema.model_rebuild()
GradeRelationshipSchema.model_rebuild()
GradeWithRelationshipsSchema.model_rebuild()
MarkListSchema.model_rebuild()
SavedQueryViewSchema.model_rebuild()
SavedQueryViewRelationshipSchema.model_rebuild()
SectionSchema.model_rebuild()
SectionRelationshipSchema.model_rebuild()
SectionSchemaWithRelationships.model_rebuild()
StreamSchema.model_rebuild()
StreamRelationshipSchema.model_rebuild()
StudentSchema.model_rebuild()
StudentWithRelationshipsSchema.model_rebuild()
StudentRelationshipSchema.model_rebuild()
StudentTermRecordSchema.model_rebuild()
StudentTermRecordRelationshipSchema.model_rebuild()
StudentYearRecordSchema.model_rebuild()
StudentYearRecordRelationshipSchema.model_rebuild()
SubjectSchema.model_rebuild()
SubjectRelationshipSchema.model_rebuild()
SubjectWithRelationshipsSchema.model_rebuild()
SubjectYearlyAverageSchema.model_rebuild()
SubjectYearlyAverageRelationshipSchema.model_rebuild()
TeacherRecordSchema.model_rebuild()
TeacherRecordRelationshipSchema.model_rebuild()
TeacherSchema.model_rebuild()
TeacherRelationshipSchema.model_rebuild()
TeacherWithRelationshipsSchema.model_rebuild()
UserSchema.model_rebuild()
UserRelationshipSchema.model_rebuild()
UserWithRelationshipsSchema.model_rebuild()
YearSchema.model_rebuild()
YearRelationshipSchema.model_rebuild()
YearSchemaWithRelationships.model_rebuild()
YearlySubjectSchema.model_rebuild()
YearlySubjectRelationshipSchema.model_rebuild()
