#!/usr/bin/env bash
# Launch the FastAPI dashboard with reload enabled.
uvicorn dashboard.api.main:app --reload
