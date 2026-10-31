"""Unit tests for GeoSentinel Health and Telemetry APIs."""

from backend.app.main import health_check
from backend.app.api.telemetry import get_telemetry


def test_health_endpoint():
    data = health_check()
    assert data["status"] == "HEALTHY"
    assert data["service"] == "GeoSentinel"
    assert "version" in data
    assert "aws_mode" in data


def test_telemetry_endpoint():
    data = get_telemetry()
    assert "orbitalSync" in data
    assert data["orbitalSync"].startswith("T-")
    assert data["orbitalSync"].endswith("ZULU")
    assert data["missionPhase"].startswith("ACTIVE PASS")
    assert data["ingestRateEps"] > 2000
    assert data["monitoredNodes"] == 142850
    assert data["activeHotspots"] == 384
