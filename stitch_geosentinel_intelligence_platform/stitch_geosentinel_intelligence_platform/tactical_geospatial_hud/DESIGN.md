---
name: Tactical Geospatial HUD
colors:
  surface: '#0e131e'
  surface-dim: '#0e131e'
  surface-bright: '#343946'
  surface-container-lowest: '#090e19'
  surface-container-low: '#161b27'
  surface-container: '#1b1f2b'
  surface-container-high: '#252a36'
  surface-container-highest: '#303541'
  on-surface: '#dee2f2'
  on-surface-variant: '#bbc9ce'
  inverse-surface: '#dee2f2'
  inverse-on-surface: '#2b303d'
  outline: '#859398'
  outline-variant: '#3c494d'
  surface-tint: '#00d9ff'
  primary: '#afecff'
  on-primary: '#003641'
  primary-container: '#00d9ff'
  on-primary-container: '#005b6c'
  inverse-primary: '#00687b'
  secondary: '#4edea3'
  on-secondary: '#003824'
  secondary-container: '#00a572'
  on-secondary-container: '#00311f'
  tertiary: '#ffddb8'
  on-tertiary: '#472a00'
  tertiary-container: '#ffb95f'
  on-tertiary-container: '#754900'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#aeecff'
  primary-fixed-dim: '#00d9ff'
  on-primary-fixed: '#001f26'
  on-primary-fixed-variant: '#004e5d'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#ffddb8'
  tertiary-fixed-dim: '#ffb95f'
  on-tertiary-fixed: '#2a1700'
  on-tertiary-fixed-variant: '#653e00'
  background: '#0e131e'
  on-background: '#dee2f2'
  surface-variant: '#303541'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: 0em
  body-lg:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
    letterSpacing: 0em
  body-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: 0.005em
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: 0.01em
  mono-metric-lg:
    fontFamily: JetBrains Mono
    fontSize: 22px
    fontWeight: '500'
    lineHeight: 28px
    letterSpacing: -0.02em
  mono-metric-md:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0em
  mono-metric-sm:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-caps:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.08em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 0.75rem
  margin: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1rem
  space-xl: 1.5rem
---

## Brand & Style

This design system delivers an austere, mission-critical operational atmosphere engineered for geospatial intelligence, environmental surveillance, and planetary telemetry operations. It merges the ergonomics of advanced tactical aerospace glass cockpits with high-density enterprise GIS analysis suites. 

### Visual Ethos
- **Precision Technical Minimalism**: Clean, purposeful visual hierarchy that strips away decorative bloat. Every line, badge, and glow represents an actionable data state.
- **Glassmorphic Tactical HUD**: Translucent, structural overlays hover cleanly above dynamic vector cartography without obscuring critical spatial intelligence.
- **Information-Dense Utility**: Tailored for operators monitoring thousands of concurrent raster layers, active sensors, and environmental anomaly vectors. Visual priority is dictated strictly by severity and spatial relevance.

## Colors

The palette operates in high-contrast optical tiers designed for extended low-light operations and high-resolution spatial rendering.

### Palette Architecture
- **Base Canvas (`#080D18`)**: Deep obsidian-navy void that anchors cartographic raster tiles and minimizes eye fatigue during prolonged watchstanding.
- **Surface Elevation 1 (`#0D1424`)**: Base backdrop for panels, dock rails, and bottom telemetry drawers.
- **Surface Elevation 2 (`#111827`)**: Elevated actionable cards, HUD popovers, contextual tooltips, and floating widgets.
- **Borders & Reticles (`#1F2937`)**: Crisp structural lines with 60% default opacity for understated geometric separation.
- **Primary Cyan (`#00D9FF`)**: Active telemetry vectors, selected geometries, primary actuators, active coordinate crosshairs, and focus states.
- **Secondary Emerald (`#10B981`)**: Nominal telemetry readings, verified environmental compliance, baseline stability, and confirmed sensor links.
- **Warning Amber (`#F59E0B`)**: Predictive threshold breaches, spatial drift warnings, and environmental advisories.
- **Critical Risk Rose (`#EF4444`)**: Uncontained environmental anomalies, deforestation alerts, sensor failure states, and perimeter breaches.
- **Data Neutral Muted (`#64748B` to `#94A3B8`)**: Secondary axes, spatial grids, scale bars, and unselected sensor IDs.

## Typography

Typography prioritizes fast numerical scannability, positional clarity, and zero layout shift during real-time data streaming.

### Usage Standards
- **Inter (Headlines & Spatial Body)**: Neutral geometric proportions providing legibility across multi-column data inspectors, layer lists, and filter criteria.
- **JetBrains Mono (Telemetry, Coordinates, & Timestamps)**: Mandatory for all tabular metrics, latitude/longitude coordinates (MGRS, WGS84), UTC timestamps, delta indicators, and system metadata. Monospaced tabular alignment ensures data values update smoothly without jitter.
- **Capitalization & Optical Scale**: Status indicators and system mode badges leverage `label-caps` in full uppercase with expanded letter-spacing for instantaneous identification at small physical footprints.

## Layout & Spacing

Layouts follow a viewport-anchored, fluid-grid workspace centered around an edge-to-edge cartographic canvas.

### Layout Topology
- **Viewport Canvas**: The map engine occupies 100vw × 100vh underneath modular floating HUD shells.
- **Spatial Panels**: Docked rails (280px–360px fixed width) host the Layer Catalog, Risk Index, and Sensor Query Trees.
- **Floating Overlays**: Pinned toolbars, telemetry ribbons, and coordinate indicators float with a strict `margin` of 1rem (`16px`) from outer viewport borders.
- **Compact Rhythm**: Spacing is engineered for high-density analysis. The baseline step is 4px (`space-xs`), with a standard internal card padding of 12px (`space-md`). Multi-panel gaps use 12px (`gutter`) to preserve screen real estate for the underlying map.

## Elevation & Depth

Depth is established via tactical glassmorphism, surface tinting, and precise luminescent hairline borders rather than diffuse, muddy drop shadows.

### Elevation Hierarchy
- **Level 0 (Map Floor)**: Native WebGL vector and satellite tile streams.
- **Level 1 (Docked Consoles & Bottom Telemetry Bars)**: Surface `#0D1424` at 92% opacity with `backdrop-filter: blur(12px)` and a 1px border of `#1F2937`.
- **Level 2 (Floating Action Panels & Inspector Cards)**: Surface `#111827` at 85% opacity with `backdrop-filter: blur(16px)` and a 1px border of `#1F2937` (opacity 80%).
- **Level 3 (Tactical HUD Alerts & Popovers)**: Surface `#111827` at 95% opacity, a 1px border tinted to the alert severity (e.g., `#00D9FF` for selection, `#EF4444` for critical risk), supported by a soft 12px ambient rim glow (`rgba(0, 217, 255, 0.15)` or `rgba(239, 68, 68, 0.2)`).

## Shapes

The design system maintains a structured, low-radius architectural form factor (`roundedness: 1` — 4px baseline, 8px on container groups).

### Geometry Principles
- **Micro Radii**: 4px radius on buttons, inputs, telemetry badges, and map controls preserves structural grid cohesion and evokes military avionics hardware.
- **Panel Containers**: 8px radius on floating inspector cards and HUD drawers prevents visual interference with map boundaries.
- **Tactical Indicators**: Status pips, sensor nodes, and directional compass dials retain pure circular geometry (50% radius) to contrast with the orthogonal structural UI.

## Components

### Buttons & HUD Actuators
- **Primary Action**: Solid `#00D9FF` fill with dark `#080D18` typography (weight: 600), 4px border radius, and an optional 1px outer ring. On hover: opacity 90% with a 4px soft cyan halo.
- **Ghost/Tactical Action**: Background `rgba(17, 24, 39, 0.7)`, border 1px solid `#1F2937`, text `#00D9FF`. Hover state shifts border to `#00D9FF` and background to `rgba(0, 217, 255, 0.08)`.
- **Destructive/Emergency**: Background `rgba(239, 68, 68, 0.12)`, border 1px solid `#EF4444`, text `#EF4444`. Hover state shifts fill to `#EF4444` with `#FFFFFF` text.

### Telemetry Badges & Status Pills
- Compact inline badges built with `JetBrains Mono` at `label-caps` or `mono-metric-sm`.
- Fixed height: 20px–24px. Padding: 0 6px.
- States utilize 10% opacity fills matching the state token (Cyan, Emerald, Amber, Rose) with a 1px matching border at 40% opacity, accompanied by a 6px pulsing center pip for real-time telemetry updates.

### Map Controls & Compass Widgets
- Stacked modular clusters (Zoom, Pitch, Bearing, Layer Toggle, Geolocation).
- Background: `#0D1424` with 88% backdrop blur.
- Separators: 1px internal lines in `#1F2937`.
- Hover/Active states trigger crisp `#00D9FF` icon color shifts with no layout displacement.

### Input Fields & Spatial Query Sliders
- Background: `#080D18` inset with a 1px border of `#1F2937`.
- Focused state: 1px border `#00D9FF` with a 2px inner shadow glow `rgba(0, 217, 255, 0.1)`.
- Monospace support for coordinate queries, bounding box inputs, and timeline range scrubbers.
- Slider tracks: 2px height in `#1F2937` with an active track fill in `#00D9FF` and a 12px × 12px square or chamfered thumb.

### Data Inspector Cards & HUD Drawers
- Translucent backdrop container (`#111827`, 85% opacity, 16px blur).
- Header zone: Uppercase micro-labeling with UTC timestamp, source sensor attribution, and status badge right-aligned.
- Metric display blocks: Key value pairs featuring muted labels (`#64748B`) paired with high-contrast `mono-metric-lg` numeric values.
- Trend sparks and mini histograms render with 1.5px vector strokes in Cyan or Emerald over transparent backgrounds.