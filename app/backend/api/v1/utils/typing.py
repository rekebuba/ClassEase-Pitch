from datetime import datetime
from typing import Any, Callable, List, Optional, Tuple, Type, TypeVar, TypedDict, Union
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy import ColumnElement
from models.user import User
from models.base_model import Base, CustomTypes

T = TypeVar("T")  # Fully generic

UserT = TypeVar("UserT", bound="User")  # User is your user model class
BaseT = TypeVar("BaseT", bound="Base")


class AuthType(TypedDict):
    """for valid user data."""

    identification: str
    role: CustomTypes.RoleEnum


class PostLoadUser(TypedDict):
    """for user data after post load."""

    id: str
    role: CustomTypes.RoleEnum
    national_id: str
    image_path: Optional[str]
    created_at: Optional[str]
    table_id: Optional[str]


class RangeDict(TypedDict):
    min: Union[str, int, float]
    max: Union[str, int, float]


class FilterDict(TypedDict):
    """for filter data."""

    column_name: str
    filter_id: str
    table_id: str
    table: Optional[Type[Base]]
    range: RangeDict
    variant: str
    operator: str
    value: Union[str, int, float, datetime, RangeDict]


class SortDict(TypedDict):
    """for sort data."""

    column_name: str
    desc: bool
    table_id: str
    table: Optional[Type[Base]]


class PostFilterDict(TypedDict):
    """for filter data after post load."""

    valid_filters: List[ColumnElement[Any]]
    custom_filters: FilterDict


class PostSortDict(TypedDict):
    """for sort data after post load."""

    valid_sorts: List[ColumnElement[Any]]
    custom_sorts: SortDict


class BuiltValidFilterDict(TypedDict):
    """for filter data after building."""

    valid_filters: List[ColumnElement[Any]]
    custom_filters: List[ColumnElement[Any]]


class BuiltValidSortDict(TypedDict):
    """for sort data after building."""

    valid_sorts: List[ColumnElement[Any]]
    custom_sorts: List[ColumnElement[Any]]


class PostLoadParam(TypedDict):
    """for user data after post load."""

    filters: List[PostFilterDict]
    sorts: List[PostSortDict]
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
    studentName: str
    grade: str
    finalScore: Optional[float]
    rank: Optional[int]
    sectionI: Optional[str]
    sectionII: Optional[str]
    averageI: Optional[float]
    averageII: Optional[float]
    rankI: Optional[int]
    rankII: Optional[int]


class QueryStudentTableId(TypedDict):
    identification: str
    imagePath: str
    createdAt: str
    guardianName: str
    guardianPhone: str
    isActive: bool
    studentName: Tuple[str, str]
    grade: str


class SendAllStudents(TypedDict):
    tableId: QueryStudentTableId
    data: QueryStudentsData
