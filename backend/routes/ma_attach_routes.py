"""
ma_attach_routes.py

MA Attach analytics API routes.
"""

from pathlib import Path
import sys

from fastapi import APIRouter, HTTPException

from backend.utils.response_helpers import success_response
from backend.utils.validation_helpers import validate_period_type


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ANALYTICS_DIR = PROJECT_ROOT / "analytics"

sys.path.append(str(ANALYTICS_DIR))

from ma_attach_analytics import (  # noqa: E402
    get_ma_attach_store_summary,
    get_top_ma_attach_associates,
)


router = APIRouter(
    prefix="/api/ma-attach",
    tags=["MA Attach"],
)


@router.get("/store/{store_id}/{period_type}/summary")
def ma_attach_store_summary(
    store_id: int,
    period_type: str,
) -> dict:
    """Return official MA Attach store summary for one period."""

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

    summary = get_ma_attach_store_summary(
        store_id=store_id,
        period_type=period_type,
    )

    if summary is None:
        raise HTTPException(
            status_code=404,
            detail="No MA Attach summary found for this store and period.",
        )

    return success_response(
        data=summary,
        message="MA Attach summary retrieved successfully.",
    )


@router.get("/store/{store_id}/{period_type}/top-associates")
def ma_attach_top_associates(
    store_id: int,
    period_type: str,
    limit: int = 5,
    order_by: str = "attach_revenue",
    minimum_computers: int = 1,
) -> dict:
    """Return top MA Attach associates for one store."""

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
        "attach_revenue",
        "attach_gm",
        "upt",
        "computers",
    }

    if order_by not in allowed_order_fields:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid order_by value. "
                "Expected one of: attach_revenue, attach_gm, upt, computers."
            ),
        )

    if limit < 1 or limit > 25:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 25.",
        )

    if minimum_computers < 1 or minimum_computers > 100:
        raise HTTPException(
            status_code=400,
            detail="Minimum computers must be between 1 and 100.",
        )

    associates = get_top_ma_attach_associates(
        store_id=store_id,
        period_type=period_type,
        limit=limit,
        order_by=order_by,
        minimum_computers=minimum_computers,
    )

    return success_response(
        data={
            "store_id": store_id,
            "period_type": period_type,
            "limit": limit,
            "order_by": order_by,
            "minimum_computers": minimum_computers,
            "associates": associates,
        },
        message="Top MA Attach associates retrieved successfully.",
    )