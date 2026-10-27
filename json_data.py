import json
import random
import sys
from pathlib import Path

FILE_NAME = "Dane.json"


def write_json(directory: Path) -> None:
    """Write Dane.json with one random record; overwrites an existing file.

    The directory must already exist (it is created by the path generator).
    """
    record = {
        "Model": random.choice("ABC"),
        "Wynik": random.randint(0, 1000),
        "Czas": random.randint(0, 1000),  # seconds
    }
    with open(Path(directory) / FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(record, f)


def read_json(directory: Path) -> int:
    """Return Czas from Dane.json if Model is A, otherwise 0.

    A missing or malformed file is reported on stderr and counts as 0.
    """
    path = Path(directory) / FILE_NAME
    try:
        with open(path, encoding="utf-8") as f:
            record = json.load(f)
        if not isinstance(record, dict):
            raise ValueError("Expected a JSON object")
        if record["Model"] not in ("A", "B", "C"):
            raise ValueError("Unknown model")
        for key in ("Wynik", "Czas"):
            if type(record[key]) is not int or not 0 <= record[key] <= 1000:
                raise ValueError(f"Invalid {key}")
        return record["Czas"] if record["Model"] == "A" else 0
    except FileNotFoundError:
        print(f"Missing file: {path}", file=sys.stderr)
    except (ValueError, KeyError, TypeError):
        print(f"Malformed file: {path}", file=sys.stderr)
    return 0
