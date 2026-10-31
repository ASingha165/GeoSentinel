"""Unit tests for Environmental Analytics endpoints."""

from backend.app.api.environmental import get_environmental_summary, get_environmental_timeseries


def test_environmental_summary():
    data = get_environmental_summary()
    assert "meanTemperatureC" in data
    assert data["meanTemperatureC"] == 42.8
    assert "deltaBaselineC" in data
    assert data["deltaBaselineC"] == 4.6
    assert data["advisoryLevel"] == "LEVEL_4_CRITICAL"


def test_environmental_timeseries():
    data = get_environmental_timeseries()
    assert data["dataset"] == "MODIS_LST_CLIMATOLOGY_10YR"
    assert "series" in data
    assert len(data["series"]) == 12  # 12 months
    assert data["series"][6]["month"] == "Jul"
    assert data["series"][6]["year_2024"] == 48.4
