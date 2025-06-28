from .subject_schema import SubjectRelationshipSchema, SubjectSchema
from .grade_schema import GradeRelationshipSchema, GradeSchema
from .user_schema import UserRelationshipSchema, UserSchema
from .admin_schema import AdminRelationshipSchema, AdminSchema
from .teacher_schema import TeacherRelationshipSchema, TeacherSchema
from .student_schema import StudentRelationshipSchema, StudentSchema

UserSchema.model_rebuild()
AdminSchema.model_rebuild()
TeacherSchema.model_rebuild()
StudentSchema.model_rebuild()
GradeSchema.model_rebuild()
SubjectSchema.model_rebuild()

UserRelationshipSchema.model_rebuild()
AdminRelationshipSchema.model_rebuild()
TeacherRelationshipSchema.model_rebuild()
StudentRelationshipSchema.model_rebuild()
GradeRelationshipSchema.model_rebuild()
SubjectRelationshipSchema.model_rebuild()
