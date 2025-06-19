#!/usr/bin/python3
"""Main module for the API"""

from api import create_app
from models import storage
from typing import Optional

app = create_app("development")


@app.teardown_appcontext
def cleanup_session(exception: Optional[BaseException] = None) -> None:
    storage.session.remove()  # Clean up session after request


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    app.run(host=host, port=port, debug=True, use_reloader=False)
