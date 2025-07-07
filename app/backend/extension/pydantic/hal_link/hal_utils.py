from flask import url_for
from typing import Any, Dict, Literal, Optional
from extension.pydantic.hal_link.link_schema import Link


def hal_link(
    endpoint: str,
    method: Literal["GET", "POST", "PUT", "DELETE"] = "GET",
    params: Optional[Dict[str, Any]] = None,
    schema: Optional[Dict[str, Any]] = None,
    rel: Optional[str] = None,
    external: bool = False,
) -> Link:
    return {
        "href": url_for(endpoint, **(params or {}), _external=external),
        "method": method,
        **({"schema": schema} if schema else {}),
        **({"rel": rel} if rel else {}),
    }
