"""GeoSentinel FastAPI Application Entrypoint.

Powers tactical geospatial APIs, live telemetry, AWS Open Data streaming,
and serves the tactical web dashboard.
"""

from __future__ import annotations

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.app.core.config import settings
from backend.app.api import (
    telemetry_router,
    layers_router,
    environmental_router,
    location_router,
    aws_router
)

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Tactical Planetary Intelligence & Earth Observation Platform API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/v1/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Register v1 API Routers
API_V1_PREFIX = "/api/v1"
app.include_router(telemetry_router, prefix=API_V1_PREFIX)
app.include_router(layers_router, prefix=API_V1_PREFIX)
app.include_router(environmental_router, prefix=API_V1_PREFIX)
app.include_router(location_router, prefix=API_V1_PREFIX)
app.include_router(aws_router, prefix=API_V1_PREFIX)


@app.get("/api/v1/health", tags=["Health & Status"])
def health_check():
    """System diagnostic health check."""
    return {
        "status": "HEALTHY",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "aws_mode": "ANONYMOUS_OPEN_DATA" if settings.AWS_USE_ANONYMOUS else "AUTHENTICATED"
    }


# Mount static assets if frontend directory exists
if FRONTEND_DIR.exists():
    app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
    app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")

    @app.get("/", include_in_schema=False)
    def serve_frontend_index():
        index_file = FRONTEND_DIR / "index.html"
        return FileResponse(index_file)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host=settings.HOST, port=settings.APP_PORT, reload=settings.DEBUG)
