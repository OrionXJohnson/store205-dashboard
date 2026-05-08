"""
systems_routes.py

Systems analytics API routes.
"""

from pathlib import Path
import sys

from fastapi import APIRouter, HTTPException

from backend.utils.response_helpers import success_response
from backend.utils.validation_helpers import validate_period_type


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ANALYTICS_DIR = PROJECT_ROOT / "analytics"

sys.path.append(str(ANALYTICS_DIR))

from systems_analytics import (  # noqa: E402
    get_store_rpu_comparison,
    get_store_systems_rank,
    get_store_systems_summary,
    get_top_attach_rpu_associates,
    get_top_rpu_associates,
)


router = APIRouter(
    prefix="/api/systems",
    tags=["Systems"],
)


@router.get("/store/{store_id}/{period_type}/summary")
def store_systems_summary(
    store_id: int,
    period_type: str,
) -> dict:
    """Return Systems summary metrics for one store."""

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

    summary = get_store_systems_summary(
        store_id=store_id,
        period_type=period_type,
    )

    if not summary["found"]:
        raise HTTPException(
            status_code=404,
            detail="No Systems summary found for this store and period.",
        )

    return success_response(
        data=summary,
        message="Systems summary retrieved successfully.",
    )


@router.get("/store/{store_id}/{period_type}/top-rpu-associates")
def top_rpu_associates(
    store_id: int,
    period_type: str,
    limit: int = 5,
) -> dict:
    """Return top Systems associates by RPU for one store."""

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

    if limit < 1 or limit > 25:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 25.",
        )

    associates = get_top_rpu_associates(
        store_id=store_id,
        period_type=period_type,
        limit=limit,
    )

    return success_response(
        data={
            "store_id": store_id,
            "period_type": period_type,
            "limit": limit,
            "associates": associates,
        },
        message="Top Systems RPU associates retrieved successfully.",
    )


@router.get("/store/{store_id}/{period_type}/top-attach-associates")
def top_attach_associates(
    store_id: int,
    period_type: str,
    limit: int = 5,
    minimum_primary_units: int = 3,
) -> dict:
    """Return top Systems associates by Attach RPU for one store."""

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

    if limit < 1 or limit > 25:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 25.",
        )

    if minimum_primary_units < 1 or minimum_primary_units > 100:
        raise HTTPException(
            status_code=400,
            detail="Minimum primary units must be between 1 and 100.",
        )

    associates = get_top_attach_rpu_associates(
        store_id=store_id,
        period_type=period_type,
        limit=limit,
        minimum_primary_units=minimum_primary_units,
    )

    return success_response(
        data={
            "store_id": store_id,
            "period_type": period_type,
            "limit": limit,
            "minimum_primary_units": minimum_primary_units,
            "associates": associates,
        },
        message="Top Systems Attach RPU associates retrieved successfully.",
    )


@router.get("/top-stores/{period_type}")
def top_stores_by_systems_rpu(
    period_type: str,
    limit: int = 10,
) -> dict:
    """Return top stores by Systems RPU."""

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

    if limit < 1 or limit > 50:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 50.",
        )

    stores = get_store_rpu_comparison(
        period_type=period_type,
        limit=limit,
    )

    return success_response(
        data={
            "period_type": period_type,
            "limit": limit,
            "order_by": "rpu",
            "stores": stores,
        },
        message="Top stores Systems RPU comparison retrieved successfully.",
    )


@router.get("/store/{store_id}/{period_type}/rankings")
def store_systems_rankings(
    store_id: int,
    period_type: str,
) -> dict:
    """Return Systems rankings for key metrics."""

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
        "rpu",
        "total_attach_rpu",
        "asp",
        "primary_units",
    ]

    rankings = {}

    for metric in metrics:
        rank_info = get_store_systems_rank(
            store_id=store_id,
            period_type=period_type,
            metric=metric,
        )

        if not rank_info["found"]:
            raise HTTPException(
                status_code=404,
                detail=(
                    "No Systems ranking found "
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
        message="Store Systems rankings retrieved successfully.",
    )