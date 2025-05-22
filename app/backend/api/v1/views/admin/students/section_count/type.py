from typing import TypedDict


class countType(TypedDict):
    """for count data."""

    section: str
    total: int


class SectionCountType(TypedDict):
    """for section count data."""

    sectionI: countType
    sectionII: countType
