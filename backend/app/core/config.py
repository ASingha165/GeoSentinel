"""GeoSentinel Application Configuration.

Loads environment variables, default coordinates, S3 bucket settings,
and CORS origins using Pydantic Settings.
"""

from __future__ import annotations

import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")
    APP_NAME: str = "GeoSentinel"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "*"
    ]

    # AWS S3 Settings
    AWS_REGION: str = "us-east-1"
    AWS_USE_ANONYMOUS: bool = True
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None

    SENTINEL2_S3_BUCKET: str = "sentinel-s2-l2a"
    MODIS_S3_BUCKET: str = "modis-pds"
    NOAA_HRRR_S3_BUCKET: str = "noaa-hrrr-bdp-pds"
    LANDSAT_S3_BUCKET: str = "landsat-pds"

    # Default Spatial Settings
    DEFAULT_AOI_NAME: str = "Phoenix Metro, Arizona"
    DEFAULT_LATITUDE: float = 33.4484
    DEFAULT_LONGITUDE: float = -112.0740
    DEFAULT_ZOOM: int = 11

    # Ingestion & Telemetry Rates
    SIMULATED_INGESTION_RATE: int = 2410


settings = Settings()
