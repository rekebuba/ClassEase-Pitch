from .subject_schema import SubjectSchema
from .grade_schema import GradeSchema
from .user_schema import UserSchema
from .admin_schema import AdminSchema
from .teacher_schema import TeacherSchema
from .student_schema import StudentSchema

UserSchema.model_rebuild()
AdminSchema.model_rebuild()
TeacherSchema.model_rebuild()
StudentSchema.model_rebuild()
GradeSchema.model_rebuild()
SubjectSchema.model_rebuild()
