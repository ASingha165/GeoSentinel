"""GeoSentinel Dataset Loader & Spatial Query Helper.

Loads and parses local GeoJSON datasets, STAC metadata, and climatology
time-series records with AWS S3 streaming support.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from backend.app.aws.s3_client import aws_s3_client

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"


class DatasetLoader:
    """Manages cached access to GeoSentinel vector and raster metadata datasets."""

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or DATA_DIR
        self._cache: Dict[str, Any] = {}

    def get_phoenix_aoi(self) -> Dict[str, Any]:
        """Return Phoenix Metro AOI polygon GeoJSON."""
        return self._load_json("phoenix_aoi.geojson")

    def get_thermal_anomalies(self) -> Dict[str, Any]:
        """Return Thermal Anomalies FeatureCollection GeoJSON."""
        return self._load_json("thermal_anomalies.geojson")

    def get_sensor_clusters(self) -> Dict[str, Any]:
        """Return Sensor Cluster points FeatureCollection GeoJSON."""
        return self._load_json("sensor_clusters.geojson")

    def get_climatology_baseline(self) -> Dict[str, Any]:
        """Return LST historical climatology and multi-year time-series data."""
        return self._load_json("lst_climatology_baseline.json")

    def get_sentinel_scene(self) -> Dict[str, Any]:
        """Return authentic Sentinel-2 STAC GeoJSON FeatureCollection sourced from AWS S3."""
        stac_feature = aws_s3_client.get_scene_stac()
        # Normalize into a standard FeatureCollection for GIS map consumption
        return {
            "type": "FeatureCollection",
            "name": "Sentinel2_L2A_S3_Scene_Footprint",
            "crs": {
                "type": "name",
                "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}
            },
            "features": [stac_feature]
        }

    def filter_anomalies_by_severity(self, min_severity: str = "ALL") -> List[Dict[str, Any]]:
        """Filter thermal anomalies by severity level."""
        data = self.get_thermal_anomalies()
        features = data.get("features", [])
        if min_severity == "ALL":
            return features
        return [
            f for f in features
            if f.get("properties", {}).get("severity", "").upper() == min_severity.upper()
        ]

    def _load_json(self, filename: str) -> Dict[str, Any]:
        if filename in self._cache:
            return self._cache[filename]
        file_path = self.data_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Dataset file not found: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self._cache[filename] = data
            return data


# Global singleton instance
dataset_loader = DatasetLoader()
