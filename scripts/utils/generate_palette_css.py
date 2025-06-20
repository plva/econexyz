#!/usr/bin/env python3
"""Generate CSS variables from config/color_palette.json."""

import json
import subprocess
from pathlib import Path

def get_git_root() -> Path:
    try:
        result = subprocess.run([
            "git", "rev-parse", "--show-toplevel"
        ], capture_output=True, text=True, check=True)
        return Path(result.stdout.strip())
    except Exception:
        # Fallback to old method if git is not available
        return Path(__file__).resolve().parents[2]

ROOT = get_git_root()
CONFIG = ROOT / "config" / "color_palette.json"
OUTPUT = ROOT / "dashboard" / "web" / "palette.css"


def main() -> None:
    with open(CONFIG) as f:
        palette = json.load(f)

    lines = [":root {", "  /* Generated from config/color_palette.json */"]
    for group, colors in palette.items():
        base = group.replace("_", "-")
        for idx, color in enumerate(colors, 1):
            lines.append(f"  --{base}-{idx}: {color};")

    # Compatibility variables used in index.html
    try:
        lines.append(f"  --green: {palette['soft_ecological_greens'][0]};")
    except (KeyError, IndexError):
        pass
    try:
        lines.append(f"  --blue: {palette['tech_contrast_blues_teals'][0]};")
    except (KeyError, IndexError):
        pass
    try:
        lines.append(f"  --slate: {palette['neutral_base_slate_stone'][0]};")
    except (KeyError, IndexError):
        pass
    try:
        lines.append(f"  --background: {palette['neutral_base_slate_stone'][1]};")
    except (KeyError, IndexError):
        pass

    lines.append("}")
    OUTPUT.write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
