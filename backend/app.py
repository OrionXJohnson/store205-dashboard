"""
app.py

Main FastAPI application entry point for the Store 205 Dashboard API.

Run from project root:
    uvicorn backend.app:app --reload
"""

from fastapi import FastAPI

from backend.routes.sales_routes import router as sales_router
from backend.routes.health_routes import router as health_router
from backend.routes.systems_routes import router as systems_router


app = FastAPI(
    title="Store 205 Dashboard API",
    description="Backend API for Store 205 sales and performance analytics.",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(health_router)
app.include_router(sales_router)
app.include_router(systems_router)


@app.get("/")
def root() -> dict:
    """Return basic API information."""
    return {
        "message": "Store 205 Dashboard API",
        "status": "running",
        "docs_url": "/docs",
    }