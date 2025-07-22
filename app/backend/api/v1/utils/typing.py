from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Set, TypeVar, TypedDict, Union
from sqlalchemy import ColumnElement, UnaryExpression
from extension.enums.enum import RoleEnum
from models.user import User
from models.base.base_model import Base

T = TypeVar("T")  # Fully generic

UserT = TypeVar("UserT", bound="User")  # User is your user model class
BaseT = TypeVar("BaseT", bound="Base")

# Define the recursive type
IncEx = Union[Set[str], Dict[str, Union["IncEx", Set[str]]]]


class AuthType(TypedDict):
    """for valid user data."""

    identification: str
    role: RoleEnum


class PostLoadUser(TypedDict):
    """for user data after post load."""

    id: str
    role: RoleEnum
    national_id: str
    image_path: Optional[str]
    created_at: Optional[str]
    table_id: Optional[str]


class RangeDict(TypedDict):
    min: Union[str, int, float]
    max: Union[str, int, float]


class FilterDict(TypedDict):
    """for filter data."""

    column_name: Union[str, List[str]]
    default_filter: Optional[int]
    filter_id: str
    table_id: str
    table: Any
    range: RangeDict
    variant: str
    operator: str
    value: Union[str, int, float, datetime, RangeDict]


class SortDict(TypedDict):
    """for sort data."""

    column_name: List[str]
    default_sort: Optional[int]
    desc: bool
    table_id: str
    table: Any


class PostLoadParam(TypedDict):
    """for user data after post load."""

    filters: List[ColumnElement[Any]]
    sort: List[UnaryExpression[Any]]
    join_operator: Callable[..., ColumnElement[bool]]
    page: int
    per_page: int


class QueryStudentsData(TypedDict):
    """for all students data after post dump."""

    identification: str
    imagePath: str
    createdAt: str
    guardianName: str
    guardianPhone: str
    isActive: bool
    firstName_fatherName_grandFatherName: str
    grade: Optional[int]
    finalScore: Optional[float]
    rank: Optional[int]
    semesterOne: Optional[int]
    semesterTwo: Optional[int]
    sectionSemesterOne: Optional[str]
    sectionSemesterTwo: Optional[str]
    averageSemesterOne: Optional[float]
    averageSemesterTwo: Optional[float]
    rankSemesterOne: Optional[int]
    rankSemesterTwo: Optional[int]


class QueryStudentTableId(TypedDict):
    finalScore: str
    rank: str
    identification: str
    imagePath: str
    createdAt: str
    guardianName: str
    guardianPhone: str
    isActive: str
    firstName_fatherName_grandFatherName: str
    grade: str
    sectionSemesterOne: str
    sectionSemesterTwo: str
    averageSemesterOne: str
    averageSemesterTwo: str
    rankSemesterOne: str
    rankSemesterTwo: str


class SendAllStudents(TypedDict):
    tableId: QueryStudentTableId
    data: List[QueryStudentsData]
