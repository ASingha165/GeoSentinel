/**
 * GeoSentinel API Client
 * Connects to FastAPI backend (/api/v1) with seamless offline mock fallback.
 */

const API_BASE = window.location.origin.includes('8000') 
  ? '/api/v1' 
  : 'http://localhost:8000/api/v1';

export const ApiClient = {
  async getTelemetry() {
    try {
      const res = await fetch(`${API_BASE}/telemetry`);
      if (!res.ok) throw new Error('Network error');
      return await res.json();
    } catch {
      return {
        orbitalSync: 'T-00:00:14 ZULU',
        missionPhase: 'ACTIVE PASS (SENTINEL-2C / MODIS-A)',
        ingestRateEps: 2410,
        monitoredNodes: 142850,
        activeHotspots: 1894,
        avgLST: '42.8°C',
        highRiskZones: 12,
        latencyMs: 24,
        heapMb: 142,
        rasterTiles: 16
      };
    }
  },

  async getLayers() {
    try {
      const res = await fetch(`${API_BASE}/layers`);
      if (!res.ok) throw new Error('Network error');
      return await res.json();
    } catch {
      return [
        { id: 'thermal_ir', name: 'Thermal IR Radiance', sensor: 'MODIS v6.1', active: true, color: '#00d9ff' },
        { id: 'heat_index', name: 'Surface Heat Index', sensor: 'Sentinel-2 L2A', active: true, color: '#ffb4ab' },
        { id: 'ndvi', name: 'NDVI Canopy Index', sensor: 'Sentinel-2 MSI', active: false, color: '#4edea3' },
        { id: 'urban_canopy', name: 'Urban Canopy Deficit', sensor: 'Landsat-9 OLI', active: false, color: '#ffb95f' }
      ];
    }
  },

  async getGeoJsonLayer(layerId) {
    try {
      const res = await fetch(`${API_BASE}/layers/${layerId}/geojson`);
      if (!res.ok) throw new Error('Network error');
      return await res.json();
    } catch {
      return null; // map.js has built-in offline GeoJSON geometries
    }
  },

  async getEnvironmentalSummary() {
    try {
      const res = await fetch(`${API_BASE}/environmental/summary`);
      if (!res.ok) throw new Error('Network error');
      return await res.json();
    } catch {
      return {
        aoi: 'Phoenix Metro, Arizona',
        meanTemperatureC: 42.8,
        deltaBaselineC: 4.6,
        urbanCanopyPercent: 8.4,
        albedoAvg: 0.18,
        extremeHeatDays: 48,
        nighttimeCoolingRate: '-1.2°C/hr'
      };
    }
  },

  async getAwsDatasets() {
    try {
      const res = await fetch(`${API_BASE}/aws/datasets`);
      if (!res.ok) throw new Error('Network error');
      return await res.json();
    } catch {
      return [
        { name: 'MODIS Land Surface Temp v6.1', bucket: 's3://modis-pds', status: 'SYNCHRONIZED', latency: '42ms', records: '14.2M' },
        { name: 'Sentinel-2 L2A Multispectral', bucket: 's3://sentinel-s2-l2a', status: 'STREAMING', latency: '68ms', records: '8.9M' },
        { name: 'NOAA HRRR / ERA5 Reanalysis', bucket: 's3://noaa-hrrr-bdp-pds', status: 'SYNCHRONIZED', latency: '31ms', records: '22.1M' },
        { name: 'Landsat 8-9 Surface Reflectance', bucket: 's3://landsat-pds', status: 'IDLE', latency: '55ms', records: '5.4M' }
      ];
    }
  },

  async triggerSync(aoiName) {
    try {
      const res = await fetch(`${API_BASE}/aws/sync`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ aoi: aoiName || 'Phoenix Metro' })
      });
      return await res.json();
    } catch {
      return { success: true, message: `Sync initiated for ${aoiName || 'Phoenix Metro'} via AWS S3 Open Data.` };
    }
  }
};
