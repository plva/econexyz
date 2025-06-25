import sys
from pathlib import Path

project = "EcoNexyz"
extensions = ["myst_parser"]

html_theme = "furo"
try:
    __import__("furo")
except Exception:
    html_theme = "alabaster"

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
