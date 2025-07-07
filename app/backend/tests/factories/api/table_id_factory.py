from typing import Any
from factory import LazyAttribute
from dataclasses import dataclass
from .typed_factory import TypedFactory
from models import storage
from models.table import Table


@dataclass
class Value:
    identification: str
    createdAt: str
    firstName_fatherName_grandFatherName: str
    guardianName: str
    guardianPhone: str
    isActive: str
    grade: str
    sectionSemesterOne: str
    sectionSemesterTwo: str
    averageSemesterOne: str
    averageSemesterTwo: str
    rankSemesterOne: str
    rankSemesterTwo: str
    finalScore: str
    rank: str


class TableIdFactory(TypedFactory[Value]):
    class Meta:
        model = Value
        exclude = ("db_table",)

    db_table: Any = LazyAttribute(
        lambda _: {
            name: id for name, id in storage.session.query(Table.name, Table.id).all()
        }
    )

    identification: Any = LazyAttribute(lambda x: x.db_table["users"])
    firstName_fatherName_grandFatherName: Any = LazyAttribute(
        lambda x: x.db_table["students"]
    )
    guardianName: Any = LazyAttribute(lambda x: x.db_table["students"])
    guardianPhone: Any = LazyAttribute(lambda x: x.db_table["students"])
    isActive: Any = LazyAttribute(lambda x: x.db_table["students"])

    grade: Any = LazyAttribute(lambda x: x.db_table["grades"])
    sectionSemesterOne: Any = LazyAttribute(lambda x: x.db_table["sections"])
    sectionSemesterTwo: Any = LazyAttribute(lambda x: x.db_table["sections"])
    createdAt: Any = LazyAttribute(lambda x: x.db_table["users"])
    averageSemesterOne: Any = LazyAttribute(
        lambda x: x.db_table["student_term_records"]
    )
    averageSemesterTwo: Any = LazyAttribute(
        lambda x: x.db_table["student_term_records"]
    )
    rankSemesterOne: Any = LazyAttribute(
        lambda x: x.db_table["student_term_records"]
    )
    rankSemesterTwo: Any = LazyAttribute(
        lambda x: x.db_table["student_term_records"]
    )
    finalScore: Any = LazyAttribute(lambda x: x.db_table["student_year_records"])
    rank: Any = LazyAttribute(lambda x: x.db_table["student_year_records"])
