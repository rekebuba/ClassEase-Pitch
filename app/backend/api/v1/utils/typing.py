from datetime import datetime
from typing import Any, List, Optional, Type, TypeVar, TypedDict, Union

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

class PostLoadParam(TypedDict):
    """for user data after post load."""

    filter_flag: str
    filters: Optional[List[FilterDict]]
    valid_filters: List[ColumnElement[Any]]
    custom_filters: Optional[List[str]]
    join_operator: str
    page: int
    per_page: int
    sort: Optional[List[SortDict]]
    valid_sort: List[str]
    custom_sort: Optional[List[str]]
