from pyethiodate import EthDate  # type: ignore
from datetime import datetime


def to_camel(string: str) -> str:
    """Alias generator to convert snake_case → camelCase"""
    parts = string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


def current_EC_year() -> EthDate:
    return EthDate.date_to_ethiopian(datetime.now()).year


def current_GC_year(ethiopian_year: int) -> str:
    return f"{ethiopian_year + 7}-{ethiopian_year + 8}"


def academic_year(ethiopian_year: int) -> str:
    gregorian_year = current_GC_year(ethiopian_year)
    return f"{ethiopian_year} E.C/{gregorian_year} G.C"
