from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.health_routes import router as health_router
from backend.routes.sales_routes import router as sales_router
from backend.routes.systems_routes import router as systems_router
from backend.routes.ma_attach_routes import router as ma_attach_router


app = FastAPI(
    title="Store 205 Dashboard API",
    description="Backend API for Store 205 sales and performance analytics.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(sales_router)
app.include_router(systems_router)
app.include_router(ma_attach_router)


@app.get("/")
def root() -> dict:
    """Return basic API information."""
    return {
        "message": "Store 205 Dashboard API",
        "status": "running",
        "docs_url": "/docs",
    }