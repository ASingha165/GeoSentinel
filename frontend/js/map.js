/**
 * GeoSentinel Cartography Engine
 * Powers interactive tactical geospatial rendering with dark-tactical basemaps,
 * AOI vector polygons, radiometric heat anomalies, cluster markers, and coordinate crosshairs.
 */

export class GeoSentinelMap {
  constructor(containerId = 'tactical-map') {
    this.containerId = containerId;
    this.map = null;
    this.layers = {};
    this.activeAoi = {
      name: 'Phoenix Metro, Arizona',
      lat: 33.4484,
      lng: -112.0740,
      zoom: 11
    };
  }

  init() {
    const container = document.getElementById(this.containerId);
    if (!container) return;

    // Initialize Leaflet Map
    if (typeof L === 'undefined') {
      console.warn('Leaflet library not loaded yet.');
      return;
    }

    this.map = L.map(this.containerId, {
      center: [this.activeAoi.lat, this.activeAoi.lng],
      zoom: this.activeAoi.zoom,
      zoomControl: false,
      attributionControl: false
    });

    // Dark Tactical Basemap (CartoDB Dark Matter / Stadia / OSM Dark)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      maxZoom: 19,
      subdomains: 'abcd',
      attribution: '© OpenStreetMap © CARTO'
    }).addTo(this.map);

    this.addTacticalOverlays();
    this.setupCoordinateInspector();
  }

  addTacticalOverlays() {
    // 1. AOI Bounding Polygon (Phoenix Urban Core)
    const aoiCoords = [
      [33.58, -112.25],
      [33.62, -111.95],
      [33.35, -111.88],
      [33.30, -112.22],
      [33.42, -112.30]
    ];

    const aoiPolygon = L.polygon(aoiCoords, {
      color: '#00d9ff',
      weight: 1.5,
      dashArray: '6, 4',
      fillColor: '#00d9ff',
      fillOpacity: 0.12
    }).addTo(this.map);

    aoiPolygon.bindPopup(`
      <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px;">
        <div style="color: #00d9ff; font-weight: 600; margin-bottom: 4px;">AOI: SECTOR ALPHA</div>
        <div>REGION: Phoenix Metropolitan Area</div>
        <div>BASELINE: ERA5 10YR (+4.6°C DELTA)</div>
        <div>STATION COUNT: 28 Telemetry Nodes</div>
      </div>
    `);

    // 2. Radiometric Thermal Hotspots (Thermal IR Layer)
    const hotspots = [
      { lat: 33.450, lng: -112.070, temp: 46.2, name: 'Downtown Commercial Core', radius: 1400 },
      { lat: 33.435, lng: -112.008, temp: 48.4, name: 'Sky Harbor Runway Corridor', radius: 1900 },
      { lat: 33.510, lng: -112.130, temp: 44.1, name: 'Metrocenter Concrete Basin', radius: 1100 },
      { lat: 33.378, lng: -111.970, temp: 43.7, name: 'Tempe Industrial Park', radius: 1200 }
    ];

    const thermalGroup = L.layerGroup();
    hotspots.forEach(h => {
      const circle = L.circle([h.lat, h.lng], {
        radius: h.radius,
        color: '#ffb4ab',
        weight: 1,
        fillColor: '#93000a',
        fillOpacity: 0.45
      }).addTo(thermalGroup);

      circle.bindPopup(`
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px;">
          <div style="color: #ffb4ab; font-weight: 700; margin-bottom: 2px;">CRITICAL THERMAL ANOMALY</div>
          <div>LOCATION: ${h.name}</div>
          <div>SURFACE LST: <span style="color:#ffb4ab; font-weight:bold;">${h.temp}°C (115.5°F)</span></div>
          <div>SENSOR: MODIS Aqua / Terra v6.1</div>
          <div>TIMESTAMP: Live Ingest (T-14s)</div>
        </div>
      `);
    });

    thermalGroup.addTo(this.map);
    this.layers['thermal_ir'] = thermalGroup;

    // 3. Tactical Nodes & Cluster Markers
    const clusterGroup = L.layerGroup();
    const sensorPoints = [
      { lat: 33.48, lng: -112.08, label: '+112 Nodes', status: 'CRITICAL', color: '#ffb4ab' },
      { lat: 33.40, lng: -112.15, label: '+48 Nodes', status: 'WARNING', color: '#ffb95f' },
      { lat: 33.55, lng: -112.02, label: '+12 Nodes', status: 'NOMINAL', color: '#4edea3' }
    ];

    sensorPoints.forEach(pt => {
      const icon = L.divIcon({
        className: 'tactical-marker',
        html: `
          <div style="
            background: #161b27;
            border: 1px solid ${pt.color};
            color: ${pt.color};
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 10px;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 600;
            white-space: nowrap;
            box-shadow: 0 0 10px rgba(0,0,0,0.8);
          ">
            <span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:${pt.color}; margin-right:4px;"></span>
            ${pt.label}
          </div>
        `,
        iconSize: [80, 24],
        iconAnchor: [40, 12]
      });

      L.marker([pt.lat, pt.lng], { icon })
        .addTo(clusterGroup)
        .bindPopup(`
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px;">
            <div style="color: ${pt.color}; font-weight: 600;">SENSOR CLUSTER: ${pt.label}</div>
            <div>STATUS: ${pt.status}</div>
            <div>COORDINATES: ${pt.lat.toFixed(4)}°N, ${pt.lng.toFixed(4)}°W</div>
          </div>
        `);
    });

    clusterGroup.addTo(this.map);
    this.layers['clusters'] = clusterGroup;
  }

  setupCoordinateInspector() {
    this.map.on('mousemove', (e) => {
      const latEl = document.getElementById('cursor-lat');
      const lngEl = document.getElementById('cursor-lng');
      if (latEl && lngEl) {
        latEl.textContent = `${e.latlng.lat.toFixed(4)}° N`;
        lngEl.textContent = `${Math.abs(e.latlng.lng).toFixed(4)}° W`;
      }
    });
  }

  toggleLayer(layerId) {
    if (!this.layers[layerId]) return;
    if (this.map.hasLayer(this.layers[layerId])) {
      this.map.removeLayer(this.layers[layerId]);
      return false;
    } else {
      this.map.addLayer(this.layers[layerId]);
      return true;
    }
  }

  zoomIn() {
    if (this.map) this.map.zoomIn();
  }

  zoomOut() {
    if (this.map) this.map.zoomOut();
  }

  resetView() {
    if (this.map) this.map.setView([this.activeAoi.lat, this.activeAoi.lng], this.activeAoi.zoom);
  }
}
