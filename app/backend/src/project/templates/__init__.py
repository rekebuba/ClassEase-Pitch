import json
from pathlib import Path

# Get the path relative to this file
_path = Path(__file__).parent / "default_academic_year.json"

with _path.open("r") as f:
    TEM_DATA = json.load(f)[0]
