"""
validation_helpers.py

Shared API validation helpers.
"""

VALID_PERIODS = {
    "daily",
    "pay_period_to_date",
    "month_to_date",
    "quarter_to_date",
}


def validate_period_type(period_type: str) -> bool:
    """Return True if period type is valid."""
    return period_type in VALID_PERIODS