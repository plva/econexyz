# CSV Bank Statement Parser

The repository provides a simple helper for converting bank statement CSV files into JSON data. The utility lives in `econexyz/parsers/csv_bank.py`.

## Usage

```python
from econexyz.parsers.csv_bank import parse_bank_csv

rows = parse_bank_csv("statement.csv")
print(rows)
```

`rows` is a list of dictionaries using the header row as keys. To output JSON, run `json.dumps(rows, indent=2)`.

### Example CSV

```
Date,Description,Amount
2024-01-01,Coffee,-3.50
2024-01-02,Salary,2000.00
```

### Related Tools

- [pandas](https://pandas.pydata.org/) for advanced CSV processing
