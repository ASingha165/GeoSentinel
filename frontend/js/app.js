/**
 * GeoSentinel Main Application Orchestrator
 * Coordinates UI routing, view transitions, telemetry engines, map initialization,
 * and user interactions.
 */

import { TelemetryEngine } from './telemetry.js';
import { GeoSentinelMap } from './map.js';
import { ApiClient } from './api.js';

class GeoSentinelApp {
  constructor() {
    this.currentView = 'command-center';
    this.telemetry = new TelemetryEngine();
    this.mapInstance = null;
  }

  init() {
    // Start live telemetry engine
    this.telemetry.start();

    // Bind navigation buttons
    this.bindNavigation();

    // Bind keyboard shortcuts (Cmd+K / Ctrl+K search)
    this.bindShortcuts();

    // Bind action actuators (Re-Index AOI, Export GeoJSON, Alert Center)
    this.bindActions();

    // Initialize map if on geospatial-explorer view
    if (this.currentView === 'geospatial-explorer' || document.getElementById('tactical-map')) {
      this.initMap();
    }
  }

  bindNavigation() {
    const navLinks = document.querySelectorAll('nav a[data-path]');
    navLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetView = link.getAttribute('data-path');
        this.switchView(targetView);
      });
    });
  }

  switchView(viewName) {
    if (viewName === this.currentView) return;

    // Update active nav styles
    document.querySelectorAll('nav a[data-path]').forEach(link => {
      const isTarget = link.getAttribute('data-path') === viewName;
      if (isTarget) {
        link.className = "flex items-center gap-space-sm px-space-md py-space-sm rounded transition-all bg-primary-container text-on-primary-container font-semibold";
        link.setAttribute('aria-current', 'page');
      } else {
        link.className = "flex items-center gap-space-sm px-space-md py-space-sm rounded text-on-surface-variant hover:bg-surface-container hover:text-on-surface transition-all";
        link.removeAttribute('aria-current');
      }
    });

    // Toggle view containers
    document.querySelectorAll('.view-container').forEach(container => {
      if (container.id === `view-${viewName}`) {
        container.classList.remove('hidden');
      } else {
        container.classList.add('hidden');
      }
    });

    this.currentView = viewName;

    // View specific activations
    if (viewName === 'geospatial-explorer') {
      setTimeout(() => {
        if (!this.mapInstance) {
          this.initMap();
        } else if (this.mapInstance.map) {
          this.mapInstance.map.invalidateSize();
        }
      }, 100);
    }
  }

  initMap() {
    if (!this.mapInstance) {
      this.mapInstance = new GeoSentinelMap('tactical-map');
      this.mapInstance.init();

      // Hook up map controls
      const btnZoomIn = document.getElementById('btn-zoom-in');
      const btnZoomOut = document.getElementById('btn-zoom-out');
      const btnReset = document.getElementById('btn-reset-view');

      if (btnZoomIn) btnZoomIn.addEventListener('click', () => this.mapInstance.zoomIn());
      if (btnZoomOut) btnZoomOut.addEventListener('click', () => this.mapInstance.zoomOut());
      if (btnReset) btnReset.addEventListener('click', () => this.mapInstance.resetView());

      // Layer buttons
      const btnThermal = document.getElementById('btn-layer-thermal');
      if (btnThermal) {
        btnThermal.addEventListener('click', () => {
          const active = this.mapInstance.toggleLayer('thermal_ir');
          btnThermal.classList.toggle('opacity-50', !active);
        });
      }

      const btnSentinel = document.getElementById('btn-layer-sentinel');
      if (btnSentinel) {
        btnSentinel.addEventListener('click', () => {
          const active = this.mapInstance.toggleLayer('sentinel_scene');
          btnSentinel.classList.toggle('opacity-50', !active);
        });
      }

      const btnClusters = document.getElementById('btn-layer-clusters');
      if (btnClusters) {
        btnClusters.addEventListener('click', () => {
          const active = this.mapInstance.toggleLayer('clusters');
          btnClusters.classList.toggle('opacity-50', !active);
        });
      }
    }
  }

  bindShortcuts() {
    // Search input (Enter to search & fly on map)
    const searchInput = document.getElementById('header-search-input') || document.querySelector('header input[type="text"]');
    if (searchInput) {
      searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          const query = searchInput.value.trim();
          if (query) {
            this.switchView('geospatial-explorer');
            setTimeout(() => {
              if (this.mapInstance) {
                this.mapInstance.searchAndFocus(query);
              }
            }, 250);
          }
        }
      });
    }

    window.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (searchInput) searchInput.focus();
      }
    });
  }

  bindActions() {
    // Re-index AOI button
    const btnReindex = document.getElementById('btn-reindex-aoi');
    if (btnReindex) {
      btnReindex.addEventListener('click', async () => {
        btnReindex.disabled = true;
        btnReindex.innerHTML = `<span class="material-symbols-outlined text-[16px] animate-spin">refresh</span><span>Indexing...</span>`;
        const res = await ApiClient.triggerSync('Phoenix Metro, Arizona');
        setTimeout(() => {
          btnReindex.disabled = false;
          btnReindex.innerHTML = `<span class="material-symbols-outlined text-[16px]">sync_alt</span><span>Re-Index AOI</span>`;
          alert(res.message || 'AOI re-indexed successfully.');
        }, 1200);
      });
    }

    // Export GeoJSON button
    const btnExport = document.getElementById('btn-export-geojson');
    if (btnExport) {
      btnExport.addEventListener('click', () => {
        const dummyGeoJson = {
          type: "FeatureCollection",
          name: "GeoSentinel_AOI_Export",
          features: [
            {
              type: "Feature",
              properties: { name: "Phoenix Metro AOI", meanLST: 42.8, sensor: "MODIS_SENTINEL" },
              geometry: {
                type: "Polygon",
                coordinates: [[[-112.25, 33.58], [-111.95, 33.62], [-111.88, 33.35], [-112.22, 33.30], [-112.25, 33.58]]]
              }
            }
          ]
        };
        const blob = new Blob([JSON.stringify(dummyGeoJson, null, 2)], { type: "application/geo+json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `GeoSentinel_AOI_${Date.now()}.geojson`;
        a.click();
        URL.revokeObjectURL(url);
      });
    }
  }
}

// Bootstrap on DOM load
window.addEventListener('DOMContentLoaded', () => {
  const app = new GeoSentinelApp();
  app.init();
});
