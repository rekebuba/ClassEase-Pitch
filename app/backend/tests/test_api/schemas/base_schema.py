# Define Pydantic models for response validation
from typing import Dict, List
from pydantic import BaseModel, field_validator

from models.base_model import CustomTypes


class UserModel(BaseModel):
    imagePath: str
    role: str
    identification: str

    @field_validator("role")
    @classmethod
    def validate_role(cls, value):
        if value.lower() not in CustomTypes.RoleEnum._value2member_map_:
            raise ValueError(f"Invalid role: {value}")
        return value


class DetailModel(BaseModel):
    firstName: str
    fatherName: str
    grandFatherName: str


class DashboardUserInfoResponseModel(BaseModel):
    user: UserModel
    detail: DetailModel


class SectionCountResponseModel(BaseModel):
    sectionSemesterOne: Dict[str, int]
    sectionSemesterTwo: Dict[str, int]

    @field_validator("sectionSemesterOne", "sectionSemesterTwo")
    @classmethod
    def validate_keys(cls, data_dict: Dict[str, int | None]) -> Dict[str, int | None]:
        """Allow 'N/A' in any case (e.g., 'n/a', 'N/a')."""
        for key in data_dict.keys():
            if key.upper() == "N/A":
                continue
            if not key.isalpha():
                raise ValueError(
                    f"Key '{key}' must be alphabetic or 'N/A' (case-insensitive)"
                )
        return data_dict


class Range(BaseModel):
    min: float | None
    max: float | None


class AverageRangeResponseModel(BaseModel):
    totalAverage: Range
    averageSemesterOne: Range
    averageSemesterTwo: Range
    rank: Range
    rankSemesterOne: Range
    rankSemesterTwo: Range


class AvailableCourse(BaseModel):
    code: str
    grade: int
    name: str


class StudentSubjectToRegister(BaseModel):
    academicYear: int
    courses: List[AvailableCourse]

class RegisteredGradeResponseModel(BaseModel):
    grades: List[int]
