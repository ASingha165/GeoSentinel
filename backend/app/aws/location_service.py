"""GeoSentinel Amazon Location Service & Spatial Scaffolding.

Provides geofencing evaluation, coordinate resolution, and tracker telemetry
support using Amazon Location Service primitives.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple


class AmazonLocationHelper:
    """Helper for Amazon Location Service geofences and spatial math."""

    def __init__(self, tracker_name: str = "GeoSentinelOrbitalTracker"):
        self.tracker_name = tracker_name

    @staticmethod
    def haversine_distance_km(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
        """Calculate great-circle distance between two (lat, lon) coordinates in kilometers."""
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        radius = 6371.0  # Earth radius in kilometers

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat / 2.0) ** 2
            + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2.0) ** 2
        )
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return radius * c

    def evaluate_geofence(
        self,
        center: Tuple[float, float],
        radius_km: float,
        points: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Filter points that fall within radius_km of center."""
        results = []
        for pt in points:
            coords = pt.get("geometry", {}).get("coordinates", [])
            if len(coords) >= 2:
                lon, lat = coords[0], coords[1]
                dist = self.haversine_distance_km(center, (lat, lon))
                if dist <= radius_km:
                    enriched = dict(pt)
                    enriched["properties"] = dict(enriched.get("properties", {}))
                    enriched["properties"]["distance_km"] = round(dist, 2)
                    results.append(enriched)
        return results


# Global Amazon Location helper instance
amazon_location = AmazonLocationHelper()
