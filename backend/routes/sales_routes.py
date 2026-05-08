"""
sales_routes.py

Sales analytics API routes.
"""

from pathlib import Path
import sys

from fastapi import APIRouter, HTTPException

from backend.utils.response_helpers import success_response
from backend.utils.validation_helpers import validate_period_type


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ANALYTICS_DIR = PROJECT_ROOT / "analytics"

sys.path.append(str(ANALYTICS_DIR))

from sales_analytics import (
    get_department_sales_breakdown,
    get_no_sales_id_summary,
    get_store_sales_summary,
)

router = APIRouter(
    prefix="/api/sales",
    tags=["Sales"],
)


@router.get("/store/{store_id}/{period_type}")
def store_sales_summary(store_id: int, period_type: str) -> dict:
    """Return store sales summary for one reporting period."""
    
    if not validate_period_type(period_type):
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid period type. "
                "Expected one of: "
                "daily, pay_period_to_date, "
                "month_to_date, quarter_to_date."
            ),
        )

    summary = get_store_sales_summary(
        store_id=store_id,
        period_type=period_type,
    )

    if summary is None:
        raise HTTPException(
            status_code=404,
            detail="No sales summary found for this store and period.",
        )

    return success_response(
        data={
            "store_id": store_id,
            "period_type": period_type,
            **summary,
        },
        message="Store sales summary retrieved successfully.",
    )

@router.get("/store/{store_id}/{period_type}/departments")
def store_department_breakdown(
    store_id: int,
    period_type: str,
) -> dict:
    """Return department sales breakdown for one store."""

    if not validate_period_type(period_type):
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid period type. "
                "Expected one of: "
                "daily, pay_period_to_date, "
                "month_to_date, quarter_to_date."
            ),
        )

    breakdown = get_department_sales_breakdown(
        store_id=store_id,
        period_type=period_type,
    )

    return success_response(
        data=breakdown,
        message="Department breakdown retrieved successfully.",
    )

@router.get("/store/{store_id}/{period_type}/no-sales")
def no_sales_summary(
    store_id: int,
    period_type: str,
) -> dict:
    """Return No Sales ID summary for one store."""

    if not validate_period_type(period_type):
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid period type. "
                "Expected one of: "
                "daily, pay_period_to_date, "
                "month_to_date, quarter_to_date."
            ),
        )

    summary = get_no_sales_id_summary(
        store_id=store_id,
        period_type=period_type,
    )

    if summary is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "No No Sales ID summary found "
                "for this store and period."
            ),
        )

    return success_response(
        data=summary,
        message="No Sales ID summary retrieved successfully.",
    )