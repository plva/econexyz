#!/usr/bin/env bash
# Launch the FastAPI dashboard with reload enabled.
python -c "import fastapi, uvicorn" 2>/dev/null \
  || { echo 'FastAPI and uvicorn are required. Install with pip install -r requirements.txt'; exit 1; }
uvicorn dashboard.api.main:app --reload
