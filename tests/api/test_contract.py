import os
from pathlib import Path

import pytest
import schemathesis
from hypothesis import settings
from requests import ConnectionError

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "api" / "openapi.yaml"

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

schema = schemathesis.openapi.from_path(SCHEMA_PATH)
schema.config.base_url = BASE_URL


@schema.parametrize()
@settings(deadline=None, max_examples=50)
def test_api(case):
    try:
        response = case.call()
    except ConnectionError:
        pytest.skip("Service unavailable")  # type: ignore[call-arg]
    else:
        case.validate_response(response)
