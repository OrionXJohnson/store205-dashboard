"""
api_smoke_test.py

Runs a lightweight smoke test against the local Store 205 API.

Prerequisite:
    Start the API first:
    python -m uvicorn backend.app:app --reload

Run from project root:
    python scripts/api_smoke_test.py
"""

from urllib.error import HTTPError, URLError
from urllib.request import urlopen
import json
import sys


BASE_URL = "http://127.0.0.1:8000"


VALID_ENDPOINTS = [
    "/",
    "/api/health",
    "/api/sales/store/205/daily",
    "/api/sales/store/205/daily/departments",
    "/api/sales/store/205/daily/no-sales",
    "/api/sales/store/205/daily/rankings",
    "/api/sales/top-stores/daily?limit=5",
    "/api/systems/store/205/daily/summary",
    "/api/systems/store/205/daily/top-rpu-associates",
    "/api/systems/store/205/daily/top-attach-associates",
    "/api/systems/top-stores/daily?limit=5",
    "/api/systems/store/205/daily/rankings",
    "/api/ma-attach/store/205/daily/summary",
    "/api/ma-attach/store/205/month_to_date/top-associates",
]


INVALID_ENDPOINTS = [
    ("/api/sales/store/205/bad_period", 400),
    ("/api/systems/top-stores/daily?limit=999", 400),
    ("/api/ma-attach/store/205/bad_period/summary", 400),
]


def request_json(path: str) -> tuple[int, dict]:
    """Request an API endpoint and return status code plus parsed JSON."""
    url = f"{BASE_URL}{path}"

    try:
        with urlopen(url, timeout=10) as response:
            status_code = response.status
            payload = json.loads(response.read().decode("utf-8"))
            return status_code, payload

    except HTTPError as error:
        payload = json.loads(error.read().decode("utf-8"))
        return error.code, payload

    except URLError as error:
        print(f"ERROR: Could not connect to API at {BASE_URL}")
        print(f"Details: {error}")
        sys.exit(1)


def test_valid_endpoints() -> None:
    """Verify valid endpoints return HTTP 200."""
    print("Testing valid endpoints")
    print("-----------------------")

    for path in VALID_ENDPOINTS:
        status_code, payload = request_json(path)

        if status_code != 200:
            print(f"FAIL: {path} returned {status_code}")
            print(payload)
            sys.exit(1)

        print(f"PASS: {path}")


def test_invalid_endpoints() -> None:
    """Verify invalid endpoints return expected error status codes."""
    print("\nTesting invalid endpoints")
    print("-------------------------")

    for path, expected_status in INVALID_ENDPOINTS:
        status_code, payload = request_json(path)

        if status_code != expected_status:
            print(
                f"FAIL: {path} returned {status_code}, "
                f"expected {expected_status}"
            )
            print(payload)
            sys.exit(1)

        print(f"PASS: {path} returned {expected_status}")


def main() -> None:
    """Run API smoke tests."""
    print("Store 205 API Smoke Test")
    print("========================")

    test_valid_endpoints()
    test_invalid_endpoints()

    print("\nAll API smoke tests passed.")


if __name__ == "__main__":
    main()