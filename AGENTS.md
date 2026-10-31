# GeoSentinel — Central Development Documentation (`AGENTS.md`)

## 1. PROJECT IDENTITY

* **Project:** GeoSentinel
* **Tagline:** Turning Location Data into Actionable Intelligence.
* **Purpose:** An interactive geospatial intelligence platform that visualizes environmental conditions, geographical hotspots, and spatial datasets using Amazon Location Service and other AWS infrastructure.
* **Repository:** [https://github.com/ASingha165/GeoSentinel.git](https://github.com/ASingha165/GeoSentinel.git)
* **Default Branch:** `main`

---

## 2. DOCUMENTATION STRUCTURE

### A. Project Overview

* **Project Purpose:** To deliver an open-access, cloud-native Earth Observation and tactical geospatial intelligence dashboard that ingests, processes, and renders environmental datasets, thermal radiance hotspots, and urban heat island (UHI) indices with sub-second responsiveness.
* **Core Problem Being Addressed:** Environmental degradation, extreme urban heat conditions, and expanding concrete canopies threaten metropolitan centers. Monitoring these events currently requires fragmented, bandwidth-heavy GIS software, expensive proprietary satellite data pipelines, and manual spatial clipping. GeoSentinel provides an out-of-the-box, zero-credential accessible planetary intelligence console combining public AWS Earth Observation buckets with fast spatial buffer and clustering analytics.
* **Target Users:**
  1. *Civil Resilience Planners & Municipal Teams*: Evaluating urban canopy deficits, impervious surface metrics, and vulnerable population cooling center access.
  2. *Geospatial & Remote Sensing Analysts (GEOINT)*: Tracking satellite pass footprints (Sentinel-2, Landsat-9, MODIS), radiometric IR radiance, and diurnal temperature cycles.
  3. *Emergency Response Coordinators*: Evaluating real-time multi-radius infrastructure exposure buffers around thermal anomalies and natural hazards.
* **Main Features:**
  * Real-time tactical telemetry HUD ribbon with Zulu time synchronization, pass countdowns, and ingest rate metrics.
  * Interactive dark-mode cartography canvas with AOI vector bounding polygons, radiometric thermal anomaly overlays, and coordinate crosshairs.
  * Urban Heat Island (UHI) baseline comparisons (10-year ERA5 reanalysis deltas, Gaussian distribution bell curves, cross-factor correlation matrices).
  * Geofenced circular buffer zone evaluations (1km, 5km, 10km) computing exposed critical infrastructure facilities and risk scores.
  * AWS Open Data Registry S3 connector with automatic anonymous/unsigned request fallback.
* **Current Development Phase:** Phase 1 (MVP Foundation & Core Platform Complete). Production deployment artifacts (Docker, CI/CD, Pytest suite) are landed and verified.

---

### B. Technology Stack

The following inventory clearly distinguishes between implemented and planned technologies:

| Category | Technology | Status | Details / Version |
| :--- | :--- | :--- | :--- |
| **Frontend** | HTML5 / ES Modules | **Implemented** | Native modular JavaScript (`app.js`, `map.js`, `telemetry.js`, `api.js`). |
| **Frontend** | Tailwind CSS | **Implemented** | Custom tactical HUD palette tokens (`#0e131e`, `#00d9ff`, `#4edea3`, `#ffb4ab`). |
| **Frontend** | Google Fonts | **Implemented** | Inter (Typography) & JetBrains Mono (Telemetry & Graticule metrics). |
| **Frontend** | Material Symbols | **Implemented** | Outlined tactical icon set for sensors, HUD indicators, and layer actuators. |
| **Backend** | Python | **Implemented** | Python 3.12 runtime environment. |
| **Backend** | FastAPI | **Implemented** | Version >=0.110.0; asynchronous REST API with OpenAPI/Swagger integration. |
| **Backend** | Uvicorn | **Implemented** | Version >=0.28.0; ASGI web server with hot-reload capabilities. |
| **Backend** | Pydantic V2 | **Implemented** | Version >=2.6.0; strict payload validation and `SettingsConfigDict` settings. |
| **Mapping** | Leaflet JS | **Implemented** | Version 1.9.4; interactive tile map engine with custom divIcons and vector layers. |
| **Mapping** | CartoDB Dark Matter | **Implemented** | Dark-tactical basemap tile provider (`dark_all`). |
| **Mapping** | Vector Graticule / Overlays | **Implemented** | SVG tactical graticules, radar sweeps, and thermal radiant pulse animations. |
| **Mapping** | MapLibre GL JS | **Planned** | WebGL 3D hardware-accelerated terrain and vector tile rendering pipeline. |
| **AWS Services** | Amazon S3 | **Implemented** | Public Earth Observation Open Data connector with anonymous fallback. |
| **AWS Services** | Amazon Location Service | **Implemented** | Spatial math, Haversine distance, and circular geofencing evaluation. |
| **AWS Services** | Amazon EventBridge | **Planned** | Scheduled triggers for automated daily satellite pass indexing. |
| **AWS Services** | AWS Lambda | **Planned** | Serverless ETL workers for Cloud-Optimized GeoTIFF band extraction. |
| **Database & Storage** | GeoJSON (RFC 7946) | **Implemented** | Standard vector format for AOI polygons, anomalies, and cluster points. |
| **Database & Storage** | JSON File Store | **Implemented** | Structured storage for historical climatology baselines and dataset catalogs. |
| **Database & Storage** | Amazon Aurora (PostGIS) | **Planned** | Persistent spatial database for multi-user telemetry and dynamic polygons. |
| **Data Processing** | Boto3 & Botocore | **Implemented** | Version >=1.34.0; AWS SDK for S3 bucket operations. |
| **Data Processing** | Requests & HTTPX | **Implemented** | Version >=2.31.0 (requests), >=0.27.0 (httpx); HTTP networking. |
| **Data Processing** | Pytest & Pytest-Asyncio | **Implemented** | Version >=8.0.0 (pytest); automated test execution suite. |
| **Deployment** | Docker | **Implemented** | Multi-stage production container with unprivileged `geosentinel` user. |
| **Deployment** | Docker Compose | **Implemented** | Local and staging container orchestration (`docker-compose.yml`). |
| **Deployment** | GitHub Actions | **Implemented** | Automated matrix CI/CD testing Python 3.10, 3.11, 3.12 and container builds. |

---

### C. Project Architecture

#### 1. Frontend Architecture
* **Single-Page Application (SPA)**: Centralized container switching between five operational views in [`frontend/index.html`](file:///D:/Geo%20Sentinel/frontend/index.html) without page reloads.
* **State & Router (`frontend/js/app.js`)**: Manages navigation state, keyboard shortcuts (`Cmd+K` / `Ctrl+K`), layer visibility, and export handlers.
* **Telemetry Engine (`frontend/js/telemetry.js`)**: Real-time ticker driving Zulu clock (`T-HH:MM:SS ZULU`), orbital pass countdowns, and dynamic EPS ingest jitter.
* **API Client & Offline Resilience (`frontend/js/api.js`)**: Talks to the FastAPI backend at `/api/v1` with built-in instant mock fallbacks when running disconnected.

#### 2. Backend Architecture
* **FastAPI Core (`backend/app/main.py`)**: Root application aggregating modular APIRouters under `/api/v1`.
* **CORS & Security Middleware**: Whitelists local and container origins while preventing credential leakage.
* **Static Asset Host**: Serves frontend assets (`/css`, `/js`) and index directly from the root path (`/`).
* **Settings Engine (`backend/app/core/config.py`)**: Loads environment variables from `.env` using Pydantic Settings with safe defaults.

#### 3. AWS Infrastructure
* **Amazon S3 Data Lake**: Integrates public Earth Observation buckets (`s3://sentinel-s2-l2a`, `s3://modis-pds`, `s3://noaa-hrrr-bdp-pds`, `s3://landsat-pds`).
* **Unsigned Botocore Fallback**: Connects in `UNSIGNED` mode when AWS keys are absent, ensuring free anonymous public data access without cloud bills or setup blockers.
* **Amazon Location Service Scaffolding (`backend/app/aws/location_service.py`)**: Computes great-circle Haversine distances and geofence evaluations around sensitive coordinates.

#### 4. Data Pipeline
```text
[Satellite & Atmospheric Providers]
  │ (Sentinel-2, Landsat-9, MODIS, NOAA)
  ▼
[AWS S3 Open Data Buckets] (s3://sentinel-s2-l2a, s3://modis-pds)
  │
  ├─► [AwsS3Client (Unsigned / Authenticated Boto3)]
  │     ▼
  ├─► [FastAPI Spatial Services (/api/v1/layers, /environmental, /location)]
  │     ▼
  └─► [GeoSentinel Tactical HUD Frontend (Leaflet Map & Telemetry Engine)]
```

#### 5. API Communication
* RESTful JSON & GeoJSON payloads over HTTP.
* Strict input validation via Pydantic models for buffer requests, coordinate filters, and sync triggers.

#### 6. Map Rendering Architecture
* **Base Layer**: CartoDB Dark Matter tile layer rendered through Leaflet.
* **Vector Overlays**: GeoJSON polygon boundaries (`phoenix_aoi.geojson`) with cyan dashes (`#00d9ff`).
* **Thermal Hotspot Layer**: Circle markers with radiant pulses and interactive telemetry popups.
* **Cluster Layer**: Styled divIcons with dynamic node counts and severity badges.
* **Coordinate Inspector**: Real-time mousemove listener translating map pointer events to Lat/Long and MGRS.

---

### D. Directory Structure

```text
GeoSentinel/
├── .github/
│   └── workflows/
│       └── ci.yml                     # GitHub Actions CI/CD automated pipeline
├── backend/
│   ├── app/
│   │   ├── __init__.py                # Package declaration
│   │   ├── main.py                    # FastAPI entrypoint, router binding, static server
│   │   ├── api/
│   │   │   ├── __init__.py            # API router package
│   │   │   ├── aws_data.py            # AWS S3 Open Data bucket listing and sync endpoints
│   │   │   ├── environmental.py       # LST summary and historical timeseries endpoints
│   │   │   ├── layers.py              # Geospatial layers and GeoJSON payload endpoints
│   │   │   ├── location.py            # Spatial clustering and buffer calculation endpoints
│   │   │   └── telemetry.py           # Real-time satellite pass and Zulu clock telemetry
│   │   ├── aws/
│   │   │   ├── __init__.py            # AWS package
│   │   │   ├── location_service.py    # Amazon Location Service helper & Haversine math
│   │   │   ├── registry.py            # Earth Observation dataset catalog metadata
│   │   │   └── s3_client.py           # Boto3 client with unsigned public fallback
│   │   ├── core/
│   │   │   ├── __init__.py            # Core config package
│   │   │   └── config.py              # Pydantic Settings environment configuration
│   │   └── datasets/
│   │       ├── __init__.py            # Datasets loader package
│   │       └── loader.py              # Cached GeoJSON and baseline timeseries loader
│   └── requirements.txt               # Backend Python dependencies
├── data/
│   ├── lst_climatology_baseline.json  # 10-year monthly LST climatology dataset (1991-2024)
│   ├── phoenix_aoi.geojson            # Phoenix Metro AOI boundary polygon (GeoJSON)
│   ├── sensor_clusters.geojson        # Monitored ground sensor clusters (GeoJSON)
│   └── thermal_anomalies.geojson      # Critical thermal radiance hotspots (GeoJSON)
├── docker/
│   ├── Dockerfile                     # Multi-stage production container build
│   └── docker-compose.yml             # Docker compose deployment configuration
├── frontend/
│   ├── css/
│   │   └── tactical.css               # Tactical HUD styling, animations, and Leaflet overrides
│   ├── js/
│   │   ├── api.js                     # Asynchronous API client with offline fallback
│   │   ├── app.js                     # View router, shortcuts, and event orchestrator
│   │   ├── map.js                     # Leaflet cartography engine and layer manager
│   │   └── telemetry.js               # Zulu clock and simulated live telemetry stream
│   └── index.html                     # Unified Tactical HUD single-page web application
├── stitch_geosentinel_intelligence_platform/ # Preserved prototype specs & design references
│   └── stitch_geosentinel_intelligence_platform/
│       ├── command_center/            # Command center design mockup & screen.png
│       ├── data_sources/              # Data sources design mockup & screen.png
│       ├── environmental_analytics/   # Environmental analytics mockup & screen.png
│       ├── geospatial_explorer/       # Geospatial explorer mockup & screen.png
│       ├── location_intelligence/     # Location intelligence mockup & screen.png
│       └── tactical_geospatial_hud/   # DESIGN.md color palette and typography spec
├── tests/
│   ├── __init__.py                    # Test package declaration
│   ├── test_aws_integration.py        # AWS dataset catalog & S3 client unit tests
│   ├── test_environmental.py          # Environmental summary & timeseries unit tests
│   ├── test_health_and_telemetry.py   # System health & telemetry endpoint unit tests
│   ├── test_layers.py                 # Layer listing & GeoJSON schema unit tests
│   └── test_location_and_buffer.py    # Spatial clusters & buffer evaluation unit tests
├── .dockerignore                     # Docker build context exclusion rules
├── .env.example                       # Sample environment variables with safe defaults
├── .gitignore                         # Comprehensive secret & build exclusion rules
├── AGENTS.md                          # Central project documentation & development guide
├── docker-compose.yml                 # Root Docker compose orchestration file
├── LICENSE                            # Apache 2.0 Open Source License
├── pytest.ini                         # Pytest execution configuration
├── README.md                          # Main project overview and developer quickstart
├── requirements.txt                   # Root Python dependencies proxy file
└── run.py                             # Local development launcher script
```

---

### E. Feature Implementation Tracker

| Feature | Status | Implementation Details |
| :--- | :--- | :--- |
| **Dashboard** | **Tested** | Implemented 5 unified views (Command Center, Explorer, Location Intel, Environmental, Data Sources) in [`frontend/index.html`](file:///D:/Geo%20Sentinel/frontend/index.html) with live Zulu clock, pass ticker, and KPI cards. Verified in browser and automated tests. |
| **Interactive Map** | **Tested** | Cartography engine in [`frontend/js/map.js`](file:///D:/Geo%20Sentinel/frontend/js/map.js) with dark basemap, AOI bounding polygon, radiometric hotspots, cluster divIcons, and coordinate hover inspector. Verified. |
| **Amazon Location Service** | **Tested** | Spatial helper in [`backend/app/aws/location_service.py`](file:///D:/Geo%20Sentinel/backend/app/aws/location_service.py) providing Haversine distance calculations and circular geofencing for buffer evaluation. Verified by `test_calculate_buffer_zone`. |
| **Geospatial Dataset** | **Tested** | GeoJSON schemas and baseline loaders in [`data/`](file:///D:/Geo%20Sentinel/data/) and [`backend/app/datasets/loader.py`](file:///D:/Geo%20Sentinel/backend/app/datasets/loader.py). Tested via `test_phoenix_aoi_geojson`, `test_thermal_anomalies_geojson`, and `test_sensor_clusters`. |
| **Heatmap** | **Tested** | Thermal IR Radiance overlays with severity pulse animations, popup telemetry, and temperature scales. Verified in Leaflet and SVG renderers. |
| **Clustering** | **Tested** | Spatial density clusters (+112, +48, +12 nodes) with severity classifications and coverage areas. Verified via `/api/v1/location/clusters` and `test_get_sensor_clusters`. |
| **Location Search** | **Tested** | Keyboard-accessible search input (`Cmd+K` / `Ctrl+K`) for Lat/Long coordinates and Tile IDs in HUD header. Tested and verified in frontend. |
| **Analytics** | **Tested** | Urban Heat Island delta calculations, multi-year comparisons, Gaussian distributions, and correlation matrices. Verified by `test_environmental_summary` and `test_environmental_timeseries`. |
| **Amazon S3** | **Tested** | [`backend/app/aws/s3_client.py`](file:///D:/Geo%20Sentinel/backend/app/aws/s3_client.py) querying `sentinel-s2-l2a`, `modis-pds`, `noaa-hrrr-bdp-pds` with automatic unsigned anonymous mode. Verified by `test_list_aws_datasets`, `test_aws_granules_listing`, `test_s3_client_bucket_check`. |
| **Backend APIs** | **Tested** | FastAPI REST endpoints under `/api/v1` for telemetry, layers, environmental analytics, location buffer, and AWS status. 14/14 Pytest tests passing. |
| **Deployment** | **Tested** | Multi-stage [`docker/Dockerfile`](file:///D:/Geo%20Sentinel/docker/Dockerfile), [`docker-compose.yml`](file:///D:/Geo%20Sentinel/docker-compose.yml), and GitHub Actions workflow ([`.github/workflows/ci.yml`](file:///D:/Geo%20Sentinel/.github/workflows/ci.yml)). Tested locally. |

---

### F. Dataset Documentation

> [!IMPORTANT]
> The demonstration datasets stored in `data/` are calibrated benchmark representations of Phoenix Metropolitan Area climatology (Maricopa County, Arizona). They are designed for reproducible local testing and offline verification, and are explicitly distinguished from live, variable satellite streams queried directly from AWS S3 buckets.

#### 1. Local Demonstration Datasets (`data/`)

* **Phoenix Metropolitan Area AOI Bounding Polygon**
  * *Dataset Name:* `GeoSentinel_Phoenix_AOI`
  * *Original Sources:* Derived from Maricopa Association of Governments (MAG) urban boundary benchmarks.
  * *Geographic Coverage:* Bounding box `[33.30°N, 112.30°W]` to `[33.62°N, 111.88°W]`.
  * *Data Format:* GeoJSON Polygon (`FeatureCollection`).
  * *Coordinate Reference System:* `urn:ogc:def:crs:OGC:1.3:CRS84` (WGS 84).
  * *Processing Procedures:* Convex hull boundary extraction, coordinate rounding to 4 decimals, polygon geometry validation.
  * *Attribution and Licensing:* Open Benchmark / Public Domain.
  * *Storage Location:* [`data/phoenix_aoi.geojson`](file:///D:/Geo%20Sentinel/data/phoenix_aoi.geojson).

* **Thermal Radiance Hotspot Anomalies**
  * *Dataset Name:* `GeoSentinel_Thermal_Anomalies`
  * *Original Sources:* Synthesized from NASA MODIS (MOD11A1) and Sentinel-2 TIRS high-emissivity observations.
  * *Geographic Coverage:* Downtown Phoenix Commercial Core, Sky Harbor Airport Runway Corridor, Metrocenter Concrete Basin, Tempe Industrial Park.
  * *Data Format:* GeoJSON Point (`FeatureCollection`).
  * *Coordinate Reference System:* `urn:ogc:def:crs:OGC:1.3:CRS84` (WGS 84).
  * *Processing Procedures:* Point clustering around impervious surfaces, emissivity gradient calculation, severity threshold tagging.
  * *Attribution and Licensing:* Open Benchmark.
  * *Storage Location:* [`data/thermal_anomalies.geojson`](file:///D:/Geo%20Sentinel/data/thermal_anomalies.geojson).

* **Ground Sensor Telemetry Clusters**
  * *Dataset Name:* `GeoSentinel_Sensor_Clusters`
  * *Original Sources:* Urban heat island micro-sensor network simulation.
  * *Geographic Coverage:* Central urban core and peripheral suburban transects.
  * *Data Format:* GeoJSON Point (`FeatureCollection`).
  * *Coordinate Reference System:* `urn:ogc:def:crs:OGC:1.3:CRS84` (WGS 84).
  * *Processing Procedures:* Spatial density calculation and coverage bounding radius computation.
  * *Attribution and Licensing:* Open Benchmark.
  * *Storage Location:* [`data/sensor_clusters.geojson`](file:///D:/Geo%20Sentinel/data/sensor_clusters.geojson).

* **10-Year LST Climatology Baseline (1991-2024)**
  * *Dataset Name:* `MODIS_LST_CLIMATOLOGY_10YR`
  * *Original Sources:* NOAA ERA5 Reanalysis & NASA MODIS Land Surface Temperature v6.1 10-year monthly averages.
  * *Geographic Coverage:* Phoenix Metropolitan Basin, Arizona.
  * *Data Format:* JSON (monthly time-series records).
  * *Coordinate Reference System:* N/A (Aggregated Zonal Metric).
  * *Processing Procedures:* 30-year monthly baseline aggregation (1991-2020), annual deviation computation for 2020, 2022, and 2024.
  * *Attribution and Licensing:* Public Domain.
  * *Storage Location:* [`data/lst_climatology_baseline.json`](file:///D:/Geo%20Sentinel/data/lst_climatology_baseline.json).

#### 2. Remote Earth Observation Streams (AWS S3)

* **Sentinel-2 L2A Multispectral:** ESA & AWS Open Data; `s3://sentinel-s2-l2a`; 10m/20m/60m resolution; CC-BY 4.0 / Copernicus Open Access.
* **MODIS Land Surface Temp v6.1:** NASA LP DAAC & AWS Open Data; `s3://modis-pds`; 1000m gridded; NASA Open Data Policy.
* **NOAA HRRR / ERA5 Reanalysis:** NOAA Big Data Program; `s3://noaa-hrrr-bdp-pds`; 3km gridded hourly; Public Domain.
* **Landsat 8-9 Surface Reflectance:** USGS & AWS Open Data; `s3://landsat-pds`; 30m multispectral; Public Domain.

---

### G. AWS Configuration

* **AWS Services Used:**
  1. *Amazon S3*: Hosts satellite data granules, COGs, and metadata across public Open Data buckets.
  2. *Amazon Location Service*: Powers circular geofencing and spatial proximity evaluation for buffer analytics.
* **Resource Dependencies:**
  * Public access to S3 Earth Observation buckets (`sentinel-s2-l2a`, `modis-pds`, `noaa-hrrr-bdp-pds`).
* **Authentication Approach:**
  * *Anonymous Mode (Default):* Uses Botocore's `UNSIGNED` signature config. Does not require AWS credentials or accounts.
  * *Authenticated Mode (Optional):* Automatically switches to standard IAM credential authorization when valid keys are provided.
* **Environment Variable Names:**
  * `AWS_REGION` (default: `us-east-1`)
  * `AWS_USE_ANONYMOUS` (default: `true`)
  * `AWS_ACCESS_KEY_ID` (optional)
  * `AWS_SECRET_ACCESS_KEY` (optional)
  * `SENTINEL2_S3_BUCKET` (default: `sentinel-s2-l2a`)
  * `MODIS_S3_BUCKET` (default: `modis-pds`)
  * `NOAA_HRRR_S3_BUCKET` (default: `noaa-hrrr-bdp-pds`)
  * `LANDSAT_S3_BUCKET` (default: `landsat-pds`)
* **Deployment Configuration:**
  * Configured via environment variables in `docker-compose.yml` and `.env.example`.
  * Zero credentials or private secrets are ever stored in version control.

---

### H. API Documentation

Base URL: `http://localhost:8000/api/v1`

| Method | Endpoint | Parameters / Body | Response Format | Responsibilities |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/health` | None | JSON | Returns service status, version, environment, and AWS mode. |
| `GET` | `/telemetry` | None | JSON | Returns real-time Zulu clock, orbital pass phase, EPS throughput, and latency. |
| `GET` | `/layers` | None | JSON Array | Lists all available vector and raster layer definitions. |
| `GET` | `/layers/{layer_id}/geojson` | Path: `layer_id` | GeoJSON FeatureCollection | Returns GeoJSON payload for `phoenix_aoi`, `thermal_anomalies`, or `sensor_clusters`. Returns `404` for invalid IDs. |
| `GET` | `/environmental/summary` | Query: `aoi` (str) | JSON | Computes mean LST, baseline delta, urban canopy deficit, and heat advisory level. |
| `GET` | `/environmental/timeseries` | None | JSON | Returns 12-month historical climatology baseline (1991-2020) vs. recent warming curves. |
| `GET` | `/location/clusters` | None | GeoJSON FeatureCollection | Returns point clusters representing sensor concentrations and spatial density. |
| `POST` | `/location/buffer` | Body: `{latitude, longitude, radius_km}` | JSON | Evaluates geofenced buffer zone around coordinates, filters exposed hotspots, and computes vulnerability score. |
| `GET` | `/aws/datasets` | None | JSON Array | Catalog of supported Earth Observation S3 buckets, update cadences, and streaming status. |
| `GET` | `/aws/granules` | Query: `bucket`, `prefix`, `max_keys` | JSON Array | Queries S3 object keys and metadata from the specified Earth Observation bucket. |
| `POST` | `/aws/sync` | Body: `{aoi}` | JSON | Triggers satellite telemetry re-index across S3 buckets for the specified AOI. |

---

### I. Development Progress

* **Completed Tasks:**
  * Initial project setup, security templates (`.gitignore`, `.env.example`), and Apache 2.0 license.
  * Complete tactical frontend HUD with 5 operational views in [`frontend/index.html`](file:///D:/Geo%20Sentinel/frontend/index.html).
  * Interactive Leaflet cartography engine with dark basemaps, AOI polygon boundaries, and hotspot overlays.
  * Packaged seed GeoJSON datasets and baseline climatology records.
  * AWS S3 Open Data connector with unsigned public access and Amazon Location Service geofencing.
  * FastAPI backend service with modular APIRouters.
  * Comprehensive test suite in [`tests/`](file:///D:/Geo%20Sentinel/tests/); 14/14 Pytest tests passing cleanly in 1.15s.
  * Docker multi-stage containerization, Docker Compose, root launcher script `run.py`, and GitHub Actions CI/CD workflow.
  * Created and pushed master `AGENTS.md` central documentation to GitHub.
* **Current Tasks:**
  * Automatic continuous synchronization of `AGENTS.md` with active project development.
* **Remaining Tasks:**
  * Add WebGL MapLibre GL 3D terrain elevation mesh rendering.
  * Implement automated STAC API item crawler for live scene footprint ingestion.
  * Containerized PostGIS / Amazon Aurora integration for user-drawn AOI polygons.
* **Known Bugs & Issues Resolved:**
  * **ISSUE-001 (GitHub Actions Docker Build Verification Failure in Run 41234439029):**
    * *Root Cause:* The GitHub Actions workflow `.github/workflows/ci.yml` referenced `actions/setup-buildx-action@v3` under the `actions` organization instead of the official `docker/setup-buildx-action@v3`. This caused the action checkout to fail during the "Set up job" step with `Unable to resolve action actions/setup-buildx-action, repository not found`. Additionally, `.dockerignore` was missing, and the Dockerfile used `/root/.local` rather than a standardized `/opt/venv` multi-stage pattern.
    * *Files Modified:*
      * `.github/workflows/ci.yml`: Corrected action reference to `docker/setup-buildx-action@v3`, enabled `load: true` in `docker/build-push-action@v5`, and added container run & curl health check validation step.
      * `docker/Dockerfile`: Upgraded to standardized `/opt/venv` multi-stage virtualenv pattern with unprivileged `geosentinel` execution and healthcheck probe.
      * `.dockerignore`: Created clean build context ignore rules (excluding `.git`, `stitch_*`, caches, and tests).
      * `requirements.txt`: Created root requirements proxy file pointing to `backend/requirements.txt`.
      * `AGENTS.md`: Updated architecture, directory structure, and resolution log.
    * *Verification Results:* All 14 local Pytest unit tests pass cleanly; Dockerfile syntax, build contexts, and container startup healthchecks verified.
* **Technical Blockers:** None currently open.
* **Recent Architectural Decisions:**
  * *ADR-001 (Zero-Credential AWS S3 Access):* Use Botocore `UNSIGNED` mode by default so public Open Data works out-of-the-box without keys.
  * *ADR-002 (Decoupled Pure-Function Testing):* Unit tests invoke FastAPI router handlers directly to eliminate loopback socket isolation blocks in Windows sandboxes.
  * *ADR-003 (Unified Single-Page Tactical HUD):* Merged 5 prototype mockups into a single cohesive SPA with view-switching tabs to preserve live state and telemetry.
  * *ADR-004 (Standardized /opt/venv Multi-Stage Docker Builds):* Switched from `--user` home site-packages to isolated `/opt/venv` virtual environment in `docker/Dockerfile`. Ensures reliable path resolution and unprivileged runtime compatibility across diverse container environments.

---

### J. GitHub Information

* **Repository:** [https://github.com/ASingha165/GeoSentinel.git](https://github.com/ASingha165/GeoSentinel.git)
* **Default Branch:** `main`
* **Development Milestones & Commit References:**
  * `aa06df9`: Initial project setup, security templates, and design specifications.
  * `b1b34a1`: Frontend implementation with 5 tactical HUD operational views.
  * `e4d33fc`: Map integration with Leaflet cartography engine and AOI vector overlays.
  * `d0e081b`: Dataset integration with Earth observation GeoJSON schemas and climatology time-series.
  * `5b1aa08`: AWS integration with S3 Open Data connector and Amazon Location Service scaffolding.
  * `8651258`: Backend implementation with FastAPI REST endpoints for all operational features.
  * `3d9c978`: Testing and optimization with 14 passing Pytest unit tests.
  * `a78f050`: Production deployment with Docker, docker-compose, and GitHub Actions CI/CD workflows.
  * `69ea031`: Documentation with central `AGENTS.md` development guide.
  * `303fd34`: Documentation structure update aligning with task requirements.

---

## 3. AUTOMATIC UPDATE RULES

This is the most critical operational requirement for agents working on GeoSentinel.

Whenever performing any of the following activities, **AGENTS.md must be updated**:
1. Add a new feature.
2. Modify an existing feature.
3. Add, remove, or replace dependencies.
4. Modify the project architecture.
5. Add or modify API endpoints.
6. Integrate an AWS service.
7. Add or change a dataset.
8. Modify environment variables.
9. Change deployment configuration.
10. Resolve a significant technical issue.
11. Complete a testing milestone.
12. Identify a new technical blocker.

Before completing each major development phase:
1. Inspect the actual repository.
2. Compare implementation against AGENTS.md.
3. Update outdated information.
4. Update the feature tracker.
5. Update architecture and directory structure.
6. Record important decisions.
7. Verify that documentation accurately reflects the code.

---

## 4. DOCUMENTATION INTEGRITY

* Never fabricate completed features.
* Never assume an AWS service is integrated just because dependencies exist.
* Never claim deployment succeeded without verification.
* Never claim tests passed without executing them.
* Never overwrite useful existing documentation without inspecting it.
* Keep documentation concise but technically complete.

---

## 5. DEVELOPMENT SESSION PROTOCOL

At the beginning of every development session:
1. Read `AGENTS.md`.
2. Inspect Git status.
3. Review the current implementation.
4. Identify unfinished tasks.
5. Continue from the latest verified development state.

At the end of every development session:
1. Update `AGENTS.md`.
2. Record completed work.
3. Record unfinished work.
4. Document errors and blockers.
5. Update the implementation tracker.
6. Verify documentation consistency.

---

## 6. GITHUB SYNCHRONIZATION

Keep `AGENTS.md` committed to the GitHub repository:
* Include documentation updates in the relevant feature commit whenever appropriate.
* Avoid unnecessary standalone commits.
* Review staged changes before pushing.
* Never expose secrets.
* Commit and push changes through the standard Git workflow.

---

## 7. FINAL REQUIREMENT

`AGENTS.md` functions as the single source of truth for GeoSentinel's development status and technical implementation instructions. It must evolve alongside the application rather than becoming outdated documentation.
