import json
import os
from pathlib import Path
from typing import Any, Dict
from api import create_app
from models import storage


test_app = create_app("development")
storage.init_app(test_app)

absolute_path = Path(os.path.abspath(__file__)).parent


def write_json_file(file_name: str, **kwarg: Any) -> None:
    from dataclasses import asdict
    from tests.test_api.factories import SearchParamsFactory, TableIdFactory

    table_id = asdict(TableIdFactory.create())
    search_params = SearchParamsFactory.create_batch(
        tableId=table_id,
        get_sort=True,
        **kwarg,
        size=20,
    )

    data = [
        {
            "search_param": asdict(param),
        }
        for param in search_params
    ]

    file_path = absolute_path / file_name

    with file_path.open("w") as f:
        json.dump(data, f, indent=2)


# Read and prepare data at module level
def read_json_file() -> Dict[str, Any]:
    """Read a JSON file and return its content."""
    file_path = (Path(absolute_path / "test_file.json")).resolve()

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    raw_data: Dict[str, Any] = {}

    with file_path.open() as f:
        raw_data = json.load(f)

    if not raw_data:
        raise FileNotFoundError(f"File not found: {file_path}")

    return raw_data


def load_test_data(file_name: str, **kwarg: Any) -> list[Dict[str, Any]]:
    file_path = absolute_path / file_name

    # Check if the file exists, if not, create it
    remove_json_file(file_name)
    write_json_file(file_name, **kwarg)

    with file_path.open() as f:
        raw = json.load(f)
    # return [(entry["search_param"], entry["test_id"]) for entry in raw]
    return [entry["search_param"] for entry in raw]


def remove_json_file(file_name: str) -> None:
    absolute_path = Path(__file__).resolve().parent
    file_path = absolute_path / file_name

    if file_path.exists():
        file_path.unlink()
    else:
        print(f"File not found to remove: {file_path}")


# Load the JSON data
json_test_data = read_json_file()
