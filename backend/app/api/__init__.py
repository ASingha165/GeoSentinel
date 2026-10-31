"""API package for GeoSentinel."""
from .telemetry import router as telemetry_router
from .layers import router as layers_router
from .environmental import router as environmental_router
from .location import router as location_router
from .aws_data import router as aws_router

__all__ = [
    "telemetry_router",
    "layers_router",
    "environmental_router",
    "location_router",
    "aws_router"
]
