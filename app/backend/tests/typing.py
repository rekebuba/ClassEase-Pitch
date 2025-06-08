from typing import Dict, TypedDict, Union


class AuthHeader(TypedDict):
    apiKey: str


class Credential(TypedDict):
    header: Dict[str, str]


class RangeDict(TypedDict):
    min: Union[str, int, float]
    max: Union[str, int, float]
