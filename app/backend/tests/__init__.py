import json
import os
from pathlib import Path
from typing import Any, Dict
from api import create_app
from models import storage


test_app = create_app("testing")
storage.init_app(test_app)


# Read and prepare data at module level
def read_json_file() -> Dict[str, Any]:
    """Read a JSON file and return its content."""
    absolute_path = Path(os.path.abspath(__file__)).parent
    file_path = (Path(absolute_path / "test_file.json")).resolve()

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    raw_data: Dict[str, Any] = {}

    with file_path.open() as f:
        raw_data = json.load(f)

    if not raw_data:
        raise FileNotFoundError(f"File not found: {file_path}")

    return raw_data


# Load the JSON data
json_test_data = read_json_file()
