"""
response_helpers.py

Shared API response helpers.

Purpose:
- Keep route responses consistent.
- Avoid repeating response envelope formatting.
"""


def success_response(data: dict | list, message: str = "Success") -> dict:
    """Return a standard successful API response."""
    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error_response(message: str, details: dict | None = None) -> dict:
    """Return a standard error API response."""
    return {
        "success": False,
        "message": message,
        "details": details or {},
    }