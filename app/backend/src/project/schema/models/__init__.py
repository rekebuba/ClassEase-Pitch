from project.schema.models.academic_term_schema import (
    AcademicTermRelatedSchema,
    AcademicTermSchema,
    AcademicTermWithRelatedSchema,
)
from project.schema.models.admin_schema import (
    AdminRelatedSchema,
    AdminSchema,
    AdminWithRelatedSchema,
)
from project.schema.models.assessment_schema import (
    AssessmentRelatedSchema,
    AssessmentSchema,
)
from project.schema.models.blacklist_token_schema import BlacklistTokenSchema
from project.schema.models.event_schema import EventRelatedSchema, EventSchema, EventWithRelatedSchema
from project.schema.models.grade_schema import (
    GradeNestedSchema,
    GradeRelatedSchema,
    GradeSchema,
    GradeWithRelatedSchema,
    GradeWithSubjectSchema,
)
from project.schema.models.grade_stream_link_schema import GradeStreamLinkSchema
from project.schema.models.grade_stream_subject_schema import (
    GradeStreamSubjectSchema,
)
from project.schema.models.mark_list_schema import MarkListSchema
from project.schema.models.registration_schema import RegistrationSchema
from project.schema.models.saved_query_view_schema import (
    SavedQueryViewRelatedSchema,
    SavedQueryViewSchema,
)
from project.schema.models.section_schema import (
    SectionRelatedSchema,
    SectionSchema,
    SectionWithRelatedSchema,
)
from project.schema.models.stream_schema import (
    StreamNestedSchema,
    StreamRelatedSchema,
    StreamSchema,
    StreamWithRelatedSchema,
)
from project.schema.models.student_schema import (
    StudentRelatedSchema,
    StudentSchema,
    StudentWithRelatedSchema,
)
from project.schema.models.student_term_record_schema import (
    StudentTermRecordRelatedSchema,
    StudentTermRecordSchema,
    StudentTermRecordWithRelatedSchema,
)
from project.schema.models.student_year_record_schema import (
    StudentYearRecordRelatedSchema,
    StudentYearRecordSchema,
    StudentYearRecordWithRelatedSchema,
)
from project.schema.models.subject_schema import (
    BasicSubjectSchema,
    SubjectNestedSchema,
    SubjectRelatedSchema,
    SubjectSchema,
    SubjectWithRelatedSchema,
)
from project.schema.models.subject_yearly_average_schema import (
    SubjectYearlyAverageRelatedSchema,
    SubjectYearlyAverageSchema,
)
from project.schema.models.table_schema import TableSchema
from project.schema.models.teacher_record_schema import (
    TeacherRecordRelatedSchema,
    TeacherRecordSchema,
)
from project.schema.models.teacher_schema import (
    TeacherRelatedSchema,
    TeacherSchema,
    TeacherWithRelatedSchema,
)
from project.schema.models.user_schema import UserRelatedSchema, UserSchema, UserWithRelatedSchema
from project.schema.models.year_schema import (
    YearNestedSchema,
    YearRelatedSchema,
    YearSchema,
    YearWithRelatedSchema,
)
from project.schema.models.yearly_subject_schema import (
    YearlySubjectRelatedSchema,
    YearlySubjectSchema,
)

__all__ = [
    "AcademicTermRelatedSchema",
    "AcademicTermSchema",
    "AcademicTermWithRelatedSchema",
    "AdminRelatedSchema",
    "AdminSchema",
    "AdminWithRelatedSchema",
    "AssessmentRelatedSchema",
    "AssessmentSchema",
    "BlacklistTokenSchema",
    "EventRelatedSchema",
    "EventSchema",
    "EventWithRelatedSchema",
    "GradeNestedSchema",
    "GradeRelatedSchema",
    "GradeSchema",
    "GradeStreamLinkSchema",
    "GradeStreamSubjectSchema",
    "GradeWithRelatedSchema",
    "MarkListSchema",
    "RegistrationSchema",
    "SavedQueryViewRelatedSchema",
    "SavedQueryViewSchema",
    "SectionRelatedSchema",
    "SectionSchema",
    "SectionWithRelatedSchema",
    "StreamRelatedSchema",
    "StreamSchema",
    "StudentRelatedSchema",
    "StudentSchema",
    "StudentTermRecordRelatedSchema",
    "StudentTermRecordSchema",
    "StudentTermRecordWithRelatedSchema",
    "StudentWithRelatedSchema",
    "StudentYearRecordRelatedSchema",
    "StudentYearRecordSchema",
    "StudentYearRecordWithRelatedSchema",
    "SubjectNestedSchema",
    "SubjectRelatedSchema",
    "BasicSubjectSchema",
    "SubjectSchema",
    "SubjectWithRelatedSchema",
    "SubjectYearlyAverageRelatedSchema",
    "SubjectYearlyAverageSchema",
    "TableSchema",
    "TeacherRecordRelatedSchema",
    "TeacherRecordSchema",
    "TeacherRelatedSchema",
    "TeacherSchema",
    "TeacherWithRelatedSchema",
    "UserRelatedSchema",
    "UserSchema",
    "UserWithRelatedSchema",
    "YearNestedSchema",
    "YearRelatedSchema",
    "YearSchema",
    "YearWithRelatedSchema",
    "YearlySubjectRelatedSchema",
    "YearlySubjectSchema",
    "StreamNestedSchema",
    "GradeWithSubjectSchema",
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
GradeWithSubjectSchema.model_rebuild()
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
StreamNestedSchema.model_rebuild()
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

BasicSubjectSchema.model_rebuild()
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
UserSchema.model_rebuild()
UserRelatedSchema.model_rebuild()
UserWithRelatedSchema.model_rebuild()

YearSchema.model_rebuild()
YearRelatedSchema.model_rebuild()
YearNestedSchema.model_rebuild()
YearWithRelatedSchema.model_rebuild()

YearlySubjectSchema.model_rebuild()
YearlySubjectRelatedSchema.model_rebuild()

# Linking Schemas
GradeStreamSubjectSchema.model_rebuild()
