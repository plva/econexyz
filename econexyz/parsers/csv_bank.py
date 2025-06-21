"""Simple CSV parser for bank statements."""

from pathlib import Path
import csv
from typing import List, Dict


def parse_bank_csv(path: str | Path) -> List[Dict[str, str]]:
    """Parse a CSV file with headers and return a list of rows as dicts."""
    csv_path = Path(path)
    with csv_path.open(newline="") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]
