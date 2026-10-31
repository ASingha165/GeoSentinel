"""GeoSentinel Location Intelligence API Endpoints.

Provides spatial clustering, place search, and buffer zone calculations.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, Query
from backend.app.datasets.loader import dataset_loader
from backend.app.aws.location_service import amazon_location, local_spatial

router = APIRouter(prefix="/location", tags=["Location Intelligence"])


class BufferRequest(BaseModel):
    latitude: float = Field(default=33.4484, description="Center latitude")
    longitude: float = Field(default=-112.0740, description="Center longitude")
    radius_km: float = Field(default=5.0, description="Buffer radius in kilometers", ge=0.1, le=100.0)


@router.get("/clusters", summary="List spatial density sensor clusters")
def get_sensor_clusters() -> Dict[str, Any]:
    """Retrieve all monitored sensor clusters."""
    return dataset_loader.get_sensor_clusters()


@router.get("/search", summary="Search geographic places using Amazon Location Service or local geocoder")
def search_places(
    query: str = Query(..., description="Place name, landmark, or 'lat, lng' coordinate string"),
    bias_lat: Optional[float] = Query(default=33.4484, description="Optional bias latitude"),
    bias_lng: Optional[float] = Query(default=-112.0740, description="Optional bias longitude")
) -> Dict[str, Any]:
    """Search geographic places with transparent attribution to Amazon Location Service or local fallback."""
    bias = [bias_lng, bias_lat] if bias_lat is not None and bias_lng is not None else None
    return amazon_location.search_place(text=query, bias_position=bias)


@router.post("/buffer", summary="Calculate exposed critical infrastructure inside a buffer radius")
def calculate_buffer_zone(req: BufferRequest) -> Dict[str, Any]:
    """Evaluate geofenced points within radius_km of the provided coordinate using local spatial engine."""
    anomalies = dataset_loader.get_thermal_anomalies().get("features", [])
    exposed_hotspots = local_spatial.evaluate_geofence(
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
        "calculation_engine": "LocalSpatialEngine (Haversine Spherical Formula)",
        "exposed_hotspots_count": len(exposed_hotspots),
        "exposed_hotspots": exposed_hotspots,
        "vulnerability_score": min(100, 35 + len(exposed_hotspots) * 15)
    }
