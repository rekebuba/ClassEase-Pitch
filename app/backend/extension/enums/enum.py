from enum import Enum
from typing import Type, TypeVar

EnumT = TypeVar("EnumT", bound=Enum)


class RoleEnum(str, Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"

    @classmethod
    def enum_value(cls: Type[EnumT], value: str) -> EnumT:
        """Convert a string value to the corresponding Enum member."""
        if not isinstance(value, str):
            raise TypeError(f"Expected a string, got {type(value).__name__}")

        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"{value!r} is not a valid {cls.__name__}")


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


class StatusEnum(str, Enum):
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
