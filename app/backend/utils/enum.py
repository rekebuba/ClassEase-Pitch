from enum import Enum
from typing import TypeVar

EnumT = TypeVar("EnumT", bound=Enum)


class RoleEnum(str, Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"


class TableEnum(str, Enum):
    STUDENTS = "students"
    TEACHERS = "teachers"
    ADMIN = "admin"
    SEMESTERS = "semesters"


class EventPurposeEnum(str, Enum):
    ACADEMIC = "academic"
    CULTURAL = "cultural"
    SPORTS = "sports"
    GRADUATION = "graduation"
    ADMINISTRATION = "administration"
    NEW_SEMESTER = "new semester"
    OTHER = "other"


class EventOrganizerEnum(str, Enum):
    SCHOOL = "school"
    SCHOOL_ADMINISTRATION = "school administration"
    STUDENT_CLUB = "student club"
    EXTERNAL_ORGANIZER = "external organizer"


class EventLocationEnum(str, Enum):
    AUDITORIUM = "auditorium"
    CLASSROOM = "classroom"
    SPORTS_FIELD = "sports field"
    ONLINE = "online"
    OTHER = "other"


class EventEligibilityEnum(str, Enum):
    ALL = "all"
    STUDENTS_ONLY = "students only"
    FACULTY_ONLY = "faculty only"
    INVITATION_ONLY = "invitation only"


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"


class BloodTypeEnum(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"
    UNKNOWN = "unknown"


class MaritalStatusEnum(str, Enum):
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    WIDOWED = "widowed"
    PREFER_NOT_TO_SAY = "prefer-not-to-say"


class ExperienceYearEnum(str, Enum):
    ZERO = "0"
    ONE_TO_TWO = "1-2"
    THREE_TO_FIVE = "3-5"
    SIX_TO_TEN = "6-10"
    ELEVEN_TO_FIFTEEN = "11-15"
    SIXTEEN_TO_TWENTY = "16-20"
    TWENTY_OR_MORE = "20+"


class ScheduleEnum(str, Enum):
    FULL_TIME = "full-time"
    PART_time = "part-time"
    FLEXIBLE = "flexible-hours"
    SUBSTITUTE = "substitute"


class GradeLevelEnum(str, Enum):
    PRIMARY = "primary"
    MIDDLE_SCHOOL = "middle school"
    HIGH_SCHOOL = "high school"


class TeacherApplicationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    INTERVIEW_scheduled = "interview-scheduled"
    UNDER_REVIEW = "under-review"


class HighestDegreeEnum(str, Enum):
    BACHELORS = "bachelors"
    MASTERS = "masters"
    DOCTORATE = "doctorate"


class StudentApplicationStatusEnum(str, Enum):
    PENDING = "pending"
    UNDER_REVIEW = "under-review"
    DOCUMENTS_REQUIRED = "documents-required"
    APPROVED = "approved"
    REJECTED = "rejected"
    ENROLLED = "enrolled"


class AcademicYearStatusEnum(str, Enum):
    UPCOMING = "upcoming"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class SemesterStatusEnum(str, Enum):
    UPCOMING = "upcoming"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class GradeOneSubjectsEnum(str, Enum):
    ARTS_AND_PHYSICAL_EDUCATION = "Arts and Physical Education"
    ENVIRONMENTAL_SCIENCE = "Environmental Science"
    ENGLISH = "English"
    MATHEMATICS = "Mathematics"
    MOTHER_TONGUE = "Mother Tongue"
    AMHARIC = "Amharic"


class GradeTwoSubjectsEnum(str, Enum):
    ARTS_AND_PHYSICAL_EDUCATION = "Arts and Physical Education"
    ENVIRONMENTAL_SCIENCE = "Environmental Science"
    ENGLISH = "English"
    MATHEMATICS = "Mathematics"
    MOTHER_TONGUE = "Mother Tongue"
    AMHARIC = "Amharic"


class GradeThreeSubjectsEnum(str, Enum):
    ARTS_AND_PHYSICAL_EDUCATION = "Arts and Physical Education"
    ENVIRONMENTAL_SCIENCE = "Environmental Science"
    ENGLISH = "English"
    MATHEMATICS = "Mathematics"
    MOTHER_TONGUE = "Mother Tongue"
    AMHARIC = "Amharic"


class GradeFourSubjectsEnum(str, Enum):
    ARTS_AND_PHYSICAL_EDUCATION = "Arts and Physical Education"
    ENVIRONMENTAL_SCIENCE = "Environmental Science"
    ENGLISH = "English"
    MATHEMATICS = "Mathematics"
    MOTHER_TONGUE = "Mother Tongue"
    AMHARIC = "Amharic"


class GradeFiveSubjectsEnum(str, Enum):
    INTEGRATED_SCIENCE = "Integrated Science"
    VISUAL_ARTS_AND_MUSIC = "Visual Arts and Music"
    ENGLISH = "English"
    MATHEMATICS = "Mathematics"
    MOTHER_TONGUE = "Mother Tongue"
    AMHARIC = "Amharic"
    PHYSICAL_EDUCATION = "Physical Education"
    CIVICS_AND_ETHICAL_EDUCATION = "Civics and Ethical Education"


class GradeSixSubjectsEnum(str, Enum):
    INTEGRATED_SCIENCE = "Integrated Science"
    VISUAL_ARTS_AND_MUSIC = "Visual Arts and Music"
    ENGLISH = "English"
    MATHEMATICS = "Mathematics"
    MOTHER_TONGUE = "Mother Tongue"
    AMHARIC = "Amharic"
    PHYSICAL_EDUCATION = "Physical Education"
    CIVICS_AND_ETHICAL_EDUCATION = "Civics and Ethical Education"


class GradeSevenSubjectsEnum(str, Enum):
    SOCIAL_STUDY = "Social Study"
    VISUAL_ARTS_AND_MUSIC = "Visual Arts and Music"
    ENGLISH = "English"
    MATHEMATICS = "Mathematics"
    MOTHER_TONGUE = "Mother Tongue"
    AMHARIC = "Amharic"
    PHYSICAL_EDUCATION = "Physical Education"
    CIVICS_AND_ETHICAL_EDUCATION = "Civics and Ethical Education"
    BIOLOGY = "Biology"
    PHYSICS = "Physics"
    CHEMISTRY = "Chemistry"


class GradeEightSubjectsEnum(str, Enum):
    SOCIAL_STUDY = "Social Study"
    VISUAL_ARTS_AND_MUSIC = "Visual Arts and Music"
    ENGLISH = "English"
    MATHEMATICS = "Mathematics"
    MOTHER_TONGUE = "Mother Tongue"
    AMHARIC = "Amharic"
    PHYSICAL_EDUCATION = "Physical Education"
    CIVICS_AND_ETHICAL_EDUCATION = "Civics and Ethical Education"
    BIOLOGY = "Biology"
    PHYSICS = "Physics"
    CHEMISTRY = "Chemistry"


class GradeNineSubjectsEnum(str, Enum):
    AMHARIC_AS_SECOND_LANGUAGE = "Amharic as second language"
    ENGLISH = "English"
    MATHEMATICS = "Mathematics"
    MOTHER_TONGUE = "Mother Tongue"
    PHYSICAL_EDUCATION = "Physical Education"
    CIVICS_AND_ETHICAL_EDUCATION = "Civics and Ethical Education"
    BIOLOGY = "Biology"
    PHYSICS = "Physics"
    CHEMISTRY = "Chemistry"
    GEOGRAPHY = "Geography"
    HISTORY = "History"
    INFORMATION_TECHNOLOGY = "Information Technology"


class GradeTenSubjectsEnum(str, Enum):
    ENGLISH = "English"
    MATHEMATICS = "Mathematics"
    MOTHER_TONGUE = "Mother Tongue"
    AMHARIC = "Amharic"
    PHYSICAL_EDUCATION = "Physical Education"
    CIVICS_AND_ETHICAL_EDUCATION = "Civics and Ethical Education"
    INFORMATION_TECHNOLOGY = "Information Technology"
    BIOLOGY = "Biology"
    PHYSICS = "Physics"
    CHEMISTRY = "Chemistry"
    GEOGRAPHY = "Geography"
    HISTORY = "History"


class GradeElevenSubjectsEnum(str, Enum):
    ENGLISH = "English"
    MATHEMATICS = "Mathematics"
    MOTHER_TONGUE = "Mother Tongue"
    AMHARIC = "Amharic"
    PHYSICAL_EDUCATION = "Physical Education"
    CIVICS_AND_ETHICAL_EDUCATION = "Civics and Ethical Education"
    INFORMATION_TECHNOLOGY = "Information Technology"


class GradeTwelveSubjectsEnum(str, Enum):
    ENGLISH = "English"
    MATHEMATICS = "Mathematics"
    MOTHER_TONGUE = "Mother Tongue"
    AMHARIC = "Amharic"
    PHYSICAL_EDUCATION = "Physical Education"
    CIVICS_AND_ETHICAL_EDUCATION = "Civics and Ethical Education"
    INFORMATION_TECHNOLOGY = "Information Technology"


class SocialStreamSubjectsEnum(str, Enum):
    GEOGRAPHY = "Geography"
    HISTORY = "History"
    ECONOMICS = "Economics"
    GENERAL_BUSINESS = "General Business"


class NaturalStreamSubjectsEnum(str, Enum):
    BIOLOGY = "Biology"
    PHYSICS = "Physics"
    CHEMISTRY = "Chemistry"
    TECHNICAL_DRAWING = "Technical Drawing"


class AllSubjectsEnum(str, Enum):
    AMHARIC = "Amharic"
    AMHARIC_AS_SECOND_LANGUAGE = "Amharic as second language"
    ARTS_AND_PHYSICAL_EDUCATION = "Arts and Physical Education"
    BIOLOGY = "Biology"
    CHEMISTRY = "Chemistry"
    CIVICS_AND_ETHICAL_EDUCATION = "Civics and Ethical Education"
    ECONOMICS = "Economics"
    ENGLISH = "English"
    ENVIRONMENTAL_SCIENCE = "Environmental Science"
    GENERAL_BUSINESS = "General Business"
    GEOGRAPHY = "Geography"
    HISTORY = "History"
    INFORMATION_TECHNOLOGY = "Information Technology"
    INTEGRATED_SCIENCE = "Integrated Science"
    MATHEMATICS = "Mathematics"
    MOTHER_TONGUE = "Mother Tongue"
    PHYSICAL_EDUCATION = "Physical Education"
    PHYSICS = "Physics"
    SOCIAL_STUDY = "Social Study"
    TECHNICAL_DRAWING = "Technical Drawing"
    VISUAL_ARTS_AND_MUSIC = "Visual Arts and Music"


class StreamEnum(str, Enum):
    NATURAL = "Natural"
    SOCIAL = "Social"


class GradeEnum(str, Enum):
    GRADE_ONE = "1"
    GRADE_TWO = "2"
    GRADE_THREE = "3"
    GRADE_FOUR = "4"
    GRADE_FIVE = "5"
    GRADE_SIX = "6"
    GRADE_SEVEN = "7"
    GRADE_EIGHT = "8"
    GRADE_NINE = "9"
    GRADE_TEN = "10"
    GRADE_ELEVEN = "11"
    GRADE_TWELVE = "12"


class SectionEnum(str, Enum):
    SECTION_A = "A"
    SECTION_B = "B"
    SECTION_C = "C"


class AcademicTermEnum(str, Enum):
    FIRST_TERM = "1"
    SECOND_TERM = "2"
    THIRD_TERM = "3"
    FOURTH_TERM = "4"


class AcademicTermTypeEnum(str, Enum):
    SEMESTER = "Semester"
    QUARTER = "Quarter"


class MarkListTypeEnum(str, Enum):
    TEST = "Test"
    QUIZ = "Quiz"
    ASSIGNMENT = "Assignment"
    MIDTERM = "Midterm"
    FINAL = "Final"
