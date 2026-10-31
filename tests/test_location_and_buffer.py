"""Unit tests for Location Intelligence and Spatial Buffers."""

from backend.app.api.location import (
    get_sensor_clusters,
    calculate_buffer_zone,
    search_places,
    BufferRequest
)


def test_get_sensor_clusters():
    data = get_sensor_clusters()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) >= 3


def test_search_places_known_poi():
    resp = search_places(query="Sky Harbor", bias_lat=33.4484, bias_lng=-112.0740)
    assert resp["query"] == "Sky Harbor"
    assert len(resp["results"]) > 0
    top = resp["results"][0]
    assert "Sky Harbor" in top["label"]
    assert top["latitude"] > 33.0
    assert top["longitude"] < -110.0


def test_search_places_coordinate_input():
    resp = search_places(query="33.4500, -112.0700")
    assert len(resp["results"]) > 0
    top = resp["results"][0]
    assert top["latitude"] == 33.4500
    assert top["longitude"] == -112.0700


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
