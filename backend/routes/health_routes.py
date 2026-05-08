"""
health_routes.py

Basic API health-check routes.
"""

from fastapi import APIRouter


router = APIRouter(
    prefix="/api/health",
    tags=["Health"],
)


@router.get("")
def health_check() -> dict:
    """Return API health status."""
    return {
        "status": "ok",
        "service": "store205-dashboard-api",
    }