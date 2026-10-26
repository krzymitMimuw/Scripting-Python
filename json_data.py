import json
import random
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
