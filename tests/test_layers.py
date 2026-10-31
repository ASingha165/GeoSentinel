"""Unit tests for GeoSentinel Layer and GeoJSON endpoints."""

import pytest
from fastapi import HTTPException
from backend.app.api.layers import list_layers, get_layer_geojson


def test_list_layers():
    layers = list_layers()
    assert isinstance(layers, list)
    assert len(layers) >= 4
    layer_ids = [l["id"] for l in layers]
    assert "phoenix_aoi" in layer_ids
    assert "sentinel_scene" in layer_ids
    assert "thermal_anomalies" in layer_ids
    assert "sensor_clusters" in layer_ids


def test_phoenix_aoi_geojson():
    geojson = get_layer_geojson("phoenix_aoi")
    assert geojson["type"] == "FeatureCollection"
    assert len(geojson["features"]) > 0
    feature = geojson["features"][0]
    assert feature["geometry"]["type"] == "Polygon"
    assert "meanLST_C" in feature["properties"]


def test_sentinel_scene_geojson():
    geojson = get_layer_geojson("sentinel_scene")
    assert geojson["type"] == "FeatureCollection"
    assert len(geojson["features"]) > 0
    feature = geojson["features"][0]
    assert feature["geometry"]["type"] == "Polygon"
    assert "eo:cloud_cover" in feature["properties"] or "cloud_cover" in feature["properties"]
    assert feature["properties"]["grid:code"] == "MGRS-12SXE"


def test_thermal_anomalies_geojson():
    geojson = get_layer_geojson("thermal_anomalies")
    assert geojson["type"] == "FeatureCollection"
    assert len(geojson["features"]) >= 4
    for f in geojson["features"]:
        assert f["geometry"]["type"] == "Point"
        assert "surface_lst_c" in f["properties"]
        assert f["properties"]["surface_lst_c"] > 40.0


def test_unknown_layer_404():
    with pytest.raises(HTTPException) as exc_info:
        get_layer_geojson("unknown_layer_id")
    assert exc_info.value.status_code == 404
