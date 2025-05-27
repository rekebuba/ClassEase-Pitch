from typing import Dict, TypedDict

class AuthHeader(TypedDict):
    apiKey: str

class Credential(TypedDict):
    header: Dict[str, str]
