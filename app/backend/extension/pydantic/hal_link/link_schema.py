from pydantic import BaseModel
from typing import Any, Dict, Literal, Optional


class Link(BaseModel):
    href: str
    method: Literal["GET", "POST", "PUT", "DELETE"]
    schemas: Optional[Dict[str, Any]] = None
    rel: Optional[str] = None
