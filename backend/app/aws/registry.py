"""GeoSentinel Earth Observation Registry for AWS Open Data.

Defines catalog metadata, licensing, resolutions, and update frequencies
for supported planetary sensor programs.
"""

from __future__ import annotations

from typing import Any, Dict, List


EARTH_OBSERVATION_DATASETS: List[Dict[str, Any]] = [
    {
        "id": "sentinel-2-l2a",
        "name": "Sentinel-2 L2A Multispectral",
        "provider": "European Space Agency (ESA) & AWS Open Data",
        "s3_bucket": "sentinel-s2-l2a",
        "s3_uri": "s3://sentinel-s2-l2a",
        "spatial_resolution": "10m / 20m / 60m",
        "revisit_time_days": 5,
        "license": "CC-BY 4.0 / Copernicus Open Access",
        "status": "STREAMING",
        "latency_ms": 68,
        "format": "Cloud-Optimized GeoTIFF (COG) & JPEG 2000"
    },
    {
        "id": "modis-lst",
        "name": "MODIS Land Surface Temp v6.1 (MOD11A1 / MYD11A1)",
        "provider": "NASA LP DAAC & AWS Open Data",
        "s3_bucket": "modis-pds",
        "s3_uri": "s3://modis-pds",
        "spatial_resolution": "1000m gridded",
        "revisit_time_days": 1,
        "license": "NASA Open Data Policy",
        "status": "SYNCHRONIZED",
        "latency_ms": 42,
        "format": "HDF4 / Cloud-Optimized GeoTIFF"
    },
    {
        "id": "noaa-hrrr",
        "name": "NOAA HRRR & ERA5 Atmospheric Reanalysis",
        "provider": "NOAA Big Data Program",
        "s3_bucket": "noaa-hrrr-bdp-pds",
        "s3_uri": "s3://noaa-hrrr-bdp-pds",
        "spatial_resolution": "3km High-Resolution",
        "revisit_time_days": 0.04,  # Hourly
        "license": "Public Domain (US Government)",
        "status": "SYNCHRONIZED",
        "latency_ms": 31,
        "format": "GRIB2 / NetCDF"
    },
    {
        "id": "landsat-8-9",
        "name": "Landsat 8-9 Surface Reflectance",
        "provider": "USGS & AWS Open Data Program",
        "s3_bucket": "landsat-pds",
        "s3_uri": "s3://landsat-pds",
        "spatial_resolution": "30m Multispectral / 15m Panchromatic",
        "revisit_time_days": 8,
        "license": "Public Domain",
        "status": "STANDBY",
        "latency_ms": 55,
        "format": "Cloud-Optimized GeoTIFF (COG)"
    }
]


def get_all_datasets() -> List[Dict[str, Any]]:
    """Return all cataloged Earth Observation datasets."""
    return EARTH_OBSERVATION_DATASETS


def get_dataset_by_id(dataset_id: str) -> Dict[str, Any] | None:
    """Lookup dataset by identifier."""
    for ds in EARTH_OBSERVATION_DATASETS:
        if ds["id"] == dataset_id or ds["s3_bucket"] == dataset_id:
            return ds
    return None
