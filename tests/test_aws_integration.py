"""Unit tests for AWS S3 and Open Data Integration."""

from backend.app.api.aws_data import list_aws_datasets, list_granules, trigger_sync, SyncRequest
from backend.app.aws.s3_client import aws_s3_client


def test_list_aws_datasets():
    datasets = list_aws_datasets()
    assert isinstance(datasets, list)
    assert len(datasets) >= 4
    bucket_names = [d["s3_bucket"] for d in datasets]
    assert "sentinel-s2-l2a" in bucket_names or "sentinel-cogs" in bucket_names
    assert "modis-pds" in bucket_names


def test_aws_granules_listing():
    granules = list_granules(bucket="sentinel-cogs", prefix="", max_keys=2)
    assert isinstance(granules, list)
    assert len(granules) <= 2


def test_s3_get_scene_stac():
    scene = aws_s3_client.get_scene_stac()
    assert scene["type"] == "Feature"
    assert "id" in scene
    assert "properties" in scene
    assert "datetime" in scene["properties"]
    assert "geometry" in scene
    assert scene["geometry"]["type"] == "Polygon"


def test_aws_sync_endpoint():
    req = SyncRequest(aoi="Phoenix Metro, Arizona")
    data = trigger_sync(req)
    assert data["status"] == "SUCCESS"
    assert "active_buckets" in data


def test_s3_client_bucket_check():
    status = aws_s3_client.check_bucket_status("sentinel-cogs")
    assert status["accessible"] is True
    assert status["bucket"] == "s3://sentinel-cogs"
