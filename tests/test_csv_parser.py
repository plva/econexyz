from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from econexyz.parsers.csv_bank import parse_bank_csv


def test_parse_bank_csv():
    csv_path = Path(__file__).resolve().parent / "data" / "sample_bank.csv"
    result = parse_bank_csv(csv_path)
    expected = [
        {"Date": "2024-01-01", "Description": "Coffee", "Amount": "-3.50"},
        {"Date": "2024-01-02", "Description": "Salary", "Amount": "2000.00"},
    ]
    assert result == expected
