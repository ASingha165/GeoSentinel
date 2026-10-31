"""GeoSentinel Location Intelligence API Endpoints.

Provides spatial clustering, proximity lookups, and buffer zone calculations.
"""

from __future__ import annotations

from typing import Any, Dict, List
from pydantic import BaseModel, Field
from fastapi import APIRouter
from backend.app.datasets.loader import dataset_loader
from backend.app.aws.location_service import amazon_location

router = APIRouter(prefix="/location", tags=["Location Intelligence"])


class BufferRequest(BaseModel):
    latitude: float = Field(default=33.4484, description="Center latitude")
    longitude: float = Field(default=-112.0740, description="Center longitude")
    radius_km: float = Field(default=5.0, description="Buffer radius in kilometers", ge=0.1, le=100.0)


@router.get("/clusters", summary="List spatial density sensor clusters")
def get_sensor_clusters() -> Dict[str, Any]:
    """Retrieve all monitored sensor clusters."""
    return dataset_loader.get_sensor_clusters()


@router.post("/buffer", summary="Calculate exposed critical infrastructure inside a buffer radius")
def calculate_buffer_zone(req: BufferRequest) -> Dict[str, Any]:
    """Evaluate geofenced points within radius_km of the provided coordinate."""
    anomalies = dataset_loader.get_thermal_anomalies().get("features", [])
    exposed_hotspots = amazon_location.evaluate_geofence(
        center=(req.latitude, req.longitude),
        radius_km=req.radius_km,
        points=anomalies
    )

    return {
        "center": {
            "latitude": req.latitude,
            "longitude": req.longitude
        },
        "radius_km": req.radius_km,
        "exposed_hotspots_count": len(exposed_hotspots),
        "exposed_hotspots": exposed_hotspots,
        "vulnerability_score": min(100, 35 + len(exposed_hotspots) * 15)
    }
