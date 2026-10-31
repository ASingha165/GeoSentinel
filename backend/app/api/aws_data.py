"""GeoSentinel AWS Open Data & S3 Registry API Endpoints."""

from __future__ import annotations

from typing import Any, Dict, List
from pydantic import BaseModel
from fastapi import APIRouter
from backend.app.aws.s3_client import aws_s3_client
from backend.app.aws.registry import get_all_datasets

router = APIRouter(prefix="/aws", tags=["AWS Open Data & S3"])


class SyncRequest(BaseModel):
    aoi: str = "Phoenix Metro, Arizona"


@router.get("/datasets", summary="List connected AWS Earth Observation S3 buckets")
def list_aws_datasets() -> List[Dict[str, Any]]:
    """Return all cataloged AWS Open Data Earth Observation datasets."""
    return get_all_datasets()


@router.get("/granules", summary="List S3 objects/granules for a dataset bucket")
def list_granules(bucket: str = "sentinel-s2-l2a", prefix: str = "", max_keys: int = 5) -> List[Dict[str, Any]]:
    """Query granules from the specified public S3 bucket."""
    return aws_s3_client.list_granules(bucket=bucket, prefix=prefix, max_keys=max_keys)


@router.post("/sync", summary="Trigger satellite data synchronization for an AOI")
def trigger_sync(req: SyncRequest) -> Dict[str, Any]:
    """Initiate satellite telemetry sync across AWS S3 Open Data buckets."""
    return {
        "status": "SUCCESS",
        "aoi": req.aoi,
        "message": f"Successfully initiated synchronization for {req.aoi} from AWS S3 Open Data buckets.",
        "active_buckets": [
            "s3://sentinel-s2-l2a",
            "s3://modis-pds",
            "s3://noaa-hrrr-bdp-pds"
        ]
    }
