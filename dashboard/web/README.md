# Dashboard Web

This directory contains a very small React-based dashboard. Open `index.html` in a browser while the FastAPI server is running to see agent status and recent messages.

The color palette defined in `../../config/color_palette.json` is applied via CSS variables for a consistent look.

The palette CSS is generated automatically when you run `bootstrap.sh`, but you can also generate it manually if needed:

```bash
python ../../scripts/generate_palette_css.py
```

This writes `palette.css` which `index.html` loads for its color variables.
