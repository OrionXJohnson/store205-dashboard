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
    get_store_sales_comparison,
    get_store_sales_rank,
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


@router.get("/store/{store_id}/{period_type}/rankings")
def store_sales_rankings(
    store_id: int,
    period_type: str,
) -> dict:
    """Return Store sales rankings for key metrics."""

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

    metrics = [
        "sales_amount",
        "transaction_count",
        "average_transaction",
        "no_sales_share",
    ]

    rankings = {}

    for metric in metrics:
        rank_info = get_store_sales_rank(
            store_id=store_id,
            period_type=period_type,
            metric=metric,
        )

        if not rank_info["found"]:
            raise HTTPException(
                status_code=404,
                detail=(
                    "No sales ranking found "
                    "for this store and period."
                ),
            )

        rankings[metric] = rank_info

    return success_response(
        data={
            "store_id": store_id,
            "period_type": period_type,
            "rankings": rankings,
        },
        message="Store sales rankings retrieved successfully.",
    )


@router.get("/top-stores/{period_type}")
def top_stores_by_sales(
    period_type: str,
    limit: int = 10,
    order_by: str = "sales_amount",
) -> dict:
    """Return top stores by a selected sales metric."""

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

    allowed_order_fields = {
        "sales_amount",
        "transaction_count",
        "average_transaction",
        "no_sales_share",
    }

    if order_by not in allowed_order_fields:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid order_by value. "
                "Expected one of: "
                "sales_amount, transaction_count, "
                "average_transaction, no_sales_share."
            ),
        )

    if limit < 1 or limit > 50:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 50.",
        )

    stores = get_store_sales_comparison(
        period_type=period_type,
        limit=limit,
        order_by=order_by,
    )

    return success_response(
        data={
            "period_type": period_type,
            "order_by": order_by,
            "limit": limit,
            "stores": stores,
        },
        message="Top stores sales comparison retrieved successfully.",
    )