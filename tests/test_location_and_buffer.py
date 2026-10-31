"""Unit tests for Location Intelligence and Spatial Buffers."""

from backend.app.api.location import get_sensor_clusters, calculate_buffer_zone, BufferRequest


def test_get_sensor_clusters():
    data = get_sensor_clusters()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) >= 3


def test_calculate_buffer_zone():
    req = BufferRequest(
        latitude=33.4484,
        longitude=-112.0740,
        radius_km=10.0
    )
    data = calculate_buffer_zone(req)
    assert data["radius_km"] == 10.0
    assert data["exposed_hotspots_count"] >= 1
    assert "vulnerability_score" in data
    assert data["vulnerability_score"] >= 35
