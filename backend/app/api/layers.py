"""GeoSentinel Layers & GeoJSON API Endpoints."""

from __future__ import annotations

from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException
from backend.app.datasets.loader import dataset_loader

router = APIRouter(prefix="/layers", tags=["Spatial Layers & Cartography"])


@router.get("", summary="List available cartographic and sensor raster layers")
def list_layers() -> List[Dict[str, Any]]:
    """Return available layer definitions."""
    return [
        {
            "id": "phoenix_aoi",
            "name": "Area of Interest Bounding Polygon",
            "type": "vector_polygon",
            "active": True,
            "color": "#00d9ff"
        },
        {
            "id": "thermal_anomalies",
            "name": "Thermal IR Radiance Hotspots",
            "type": "vector_points",
            "sensor": "MODIS v6.1 / Sentinel-2",
            "active": True,
            "color": "#ffb4ab"
        },
        {
            "id": "sensor_clusters",
            "name": "Active Ground Sensor Clusters",
            "type": "vector_clusters",
            "active": True,
            "color": "#4edea3"
        }
    ]


@router.get("/{layer_id}/geojson", summary="Retrieve GeoJSON FeatureCollection for a specific layer")
def get_layer_geojson(layer_id: str) -> Dict[str, Any]:
    """Retrieve GeoJSON payload for a layer."""
    if layer_id in ("phoenix_aoi", "aoi"):
        return dataset_loader.get_phoenix_aoi()
    elif layer_id in ("thermal_anomalies", "hotspots", "thermal_ir"):
        return dataset_loader.get_thermal_anomalies()
    elif layer_id in ("sensor_clusters", "clusters"):
        return dataset_loader.get_sensor_clusters()
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Layer '{layer_id}' not found. Available: phoenix_aoi, thermal_anomalies, sensor_clusters"
        )
