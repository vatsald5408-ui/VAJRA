# -*- coding: utf-8 -*-
"""
VAJRA — Final Visual Identity & Map Transformation
AirNet-grade cartographic sophistication:
- Warm charcoal, graphite, smoky slate UI palette (NO heavy blue SaaS / cyan glow)
- Professional SVG icon system (NO emojis, NO generic AI symbols)
- True OpenStreetMap foundation with high-contrast, cartographic dark filter
- Meteorological blended weather overlays (multi-gradient convective contours, soft edges)
- Floating Mini Map Search at top-right (260px wide, connected to /osm/search)
- Refined segmented control for OBSERVED | NOWCAST in neutral warm graphite
- Editorial right panel with high hierarchy, thin dividers, warm typography
- Forecast Time Machine with Play Evolution
"""

html_code = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>VAJRA — Atmospheric Intelligence Platform</title>
  <meta name="description" content="VAJRA: High-resolution atmospheric nowcasting of severe convective storms and lightning across India." />

  <!-- Typography: Inter & Plus Jakarta Sans -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />

  <!-- Leaflet CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

  <style>
    /* ==========================================================================
       1. CARTOGRAPHIC / ATMOSPHERIC DESIGN SYSTEM (WARM GRAPHITE PALETTE)
       ========================================================================== */
    :root {
      /* Warm Charcoal & Graphite Chrome (No Heavy Blue SaaS) */
      --bg-canvas: #0e1117;
      --bg-panel: #131720;
      --bg-panel-elevated: #1a1f2c;
      --bg-panel-hover: #222938;
      --bg-input: #10141c;

      /* Subtle, Refined Borders */
      --border-subtle: rgba(255, 255, 255, 0.07);
      --border-medium: rgba(255, 255, 255, 0.13);
      --border-active: #d97706;

      /* Warm Typography Colors */
      --text-pure: #ffffff;
      --text-warm-white: #f3f4f6;
      --text-primary: #e5e7eb;
      --text-secondary: #9ca3af;
      --text-muted: #6b7280;

      /* Semantic Meteorological Colors (Only Where Data Requires) */
      --radar-c20: #0284c7;
      --radar-c35: #10b981;
      --radar-c45: #eab308;
      --radar-c55: #f97316;
      --radar-c65: #dc2626;
      --radar-core: #9333ea;

      --amber-alert: #d97706;
      --vermilion-severe: #dc2626;
      --lightning-amber: #fde047;
      --forecast-violet: #a855f7;

      --font-display: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-body: 'Inter', system-ui, -apple-system, sans-serif;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }

    body {
      background: var(--bg-canvas);
      color: var(--text-primary);
      font-family: var(--font-body);
      font-size: 13.5px;
      line-height: 1.5;
      height: 100vh;
      width: 100vw;
      overflow: hidden;
      user-select: none;
    }

    /* Scrollbars */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: var(--bg-canvas); }
    ::-webkit-scrollbar-thumb { background: #272d3b; border-radius: 2px; }

    /* ==========================================================================
       2. TOP PRODUCT HEADER (MINIMAL, ELEGANT CARTOGRAPHIC CHROME)
       ========================================================================== */
    .top-header {
      height: 60px;
      background: var(--bg-panel);
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
      z-index: 1000;
      position: relative;
    }

    .brand-group {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .brand-mark-box {
      width: 34px;
      height: 34px;
      border-radius: 6px;
      background: #1f2533;
      border: 1px solid var(--border-medium);
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .brand-mark-box svg {
      width: 20px;
      height: 20px;
      stroke: var(--text-warm-white);
      fill: none;
      stroke-width: 2;
    }

    .brand-text-wrap {
      display: flex;
      flex-direction: column;
    }

    .brand-title {
      font-family: var(--font-display);
      font-size: 19px;
      font-weight: 800;
      letter-spacing: -0.4px;
      color: var(--text-pure);
      line-height: 1.15;
    }

    .brand-subtitle {
      font-size: 11.5px;
      color: var(--text-secondary);
      font-weight: 500;
    }

    /* Header Center: Regional Atmospheric Overview */
    .regional-status-bar {
      display: flex;
      align-items: center;
      gap: 16px;
      background: var(--bg-panel-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 6px 14px;
    }

    .domain-indicator {
      display: flex;
      align-items: center;
      gap: 7px;
      font-family: var(--font-display);
      font-size: 12.5px;
      font-weight: 700;
      color: var(--text-warm-white);
    }

    .live-pulse-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 6px #10b981;
    }

    .domain-stats-summary {
      font-size: 12px;
      color: var(--text-secondary);
    }
    .domain-stats-summary strong {
      color: var(--text-pure);
      font-weight: 600;
    }

    /* Header Right Tools */
    .header-right-tools {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .btn-header-ghost {
      background: none;
      border: 1px solid var(--border-subtle);
      border-radius: 5px;
      padding: 5px 12px;
      color: var(--text-secondary);
      font-family: var(--font-display);
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
    }
    .btn-header-ghost:hover {
      background: var(--bg-panel-hover);
      color: var(--text-warm-white);
      border-color: var(--border-medium);
    }
    .btn-header-ghost.active {
      background: #272f40;
      color: var(--text-pure);
      border-color: rgba(255,255,255,0.25);
    }

    /* ==========================================================================
       3. WORKSPACE LAYOUT (LEFT CONTROLS | MAP ~70% HERO | RIGHT INTEL)
       ========================================================================== */
    .app-workspace {
      display: flex;
      height: calc(100vh - 60px);
      width: 100vw;
      position: relative;
    }

    /* ==========================================================================
       4. LEFT PANEL: CONTROLS, LAYERS & ACTIVE STORMS
       ========================================================================== */
    .left-controls-rail {
      width: 300px;
      min-width: 300px;
      background: var(--bg-panel);
      border-right: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      gap: 18px;
      padding: 18px;
      z-index: 500;
      overflow-y: auto;
    }

    .rail-section-label {
      font-family: var(--font-display);
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.6px;
      text-transform: uppercase;
      color: var(--text-muted);
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    /* Horizon Button Grid */
    .horizon-selector-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 6px;
    }

    .horizon-pill-btn {
      background: var(--bg-panel-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 5px;
      padding: 7px 4px;
      text-align: center;
      font-family: var(--font-display);
      font-size: 11.5px;
      font-weight: 600;
      color: var(--text-secondary);
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .horizon-pill-btn:hover {
      background: var(--bg-panel-hover);
      color: var(--text-warm-white);
    }
    .horizon-pill-btn.active {
      background: #2b3345;
      border-color: rgba(255, 255, 255, 0.3);
      color: var(--text-pure);
      font-weight: 700;
    }

    /* Atmospheric Layer Stack (SVG Scientific Glyphs) */
    .layer-cards-stack {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .layer-row-card {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-panel-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 9px 12px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .layer-row-card:hover {
      background: var(--bg-panel-hover);
      border-color: var(--border-medium);
    }
    .layer-row-card.active {
      border-color: rgba(255, 255, 255, 0.22);
    }

    .layer-left-info {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .layer-glyph-box {
      width: 26px;
      height: 26px;
      border-radius: 4px;
      background: #11141c;
      border: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .layer-glyph-box svg {
      width: 15px;
      height: 15px;
      stroke: var(--text-secondary);
      fill: none;
      stroke-width: 1.8;
    }
    .layer-row-card.active .layer-glyph-box svg {
      stroke: var(--text-warm-white);
    }

    .layer-title-text {
      font-size: 13px;
      font-weight: 600;
      color: var(--text-warm-white);
      line-height: 1.2;
    }
    .layer-meta-text {
      font-size: 11px;
      color: var(--text-muted);
    }

    .layer-toggle-switch {
      width: 32px;
      height: 18px;
      background: #2b3345;
      border-radius: 9px;
      position: relative;
      transition: background 0.2s;
    }
    .layer-toggle-switch::after {
      content: "";
      position: absolute;
      top: 2px;
      left: 2px;
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: #ffffff;
      transition: transform 0.2s;
    }
    .layer-row-card.active .layer-toggle-switch {
      background: #3b82f6;
    }
    .layer-row-card.active .layer-toggle-switch::after {
      transform: translateX(14px);
    }

    /* Tracked Storms Stack */
    .storms-list-stack {
      display: flex;
      flex-direction: column;
      gap: 7px;
    }

    .storm-select-card {
      background: var(--bg-panel-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 11px 12px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .storm-select-card:hover {
      background: var(--bg-panel-hover);
      border-color: var(--border-medium);
    }
    .storm-select-card.selected {
      border-color: var(--vermilion-severe);
      background: rgba(220, 38, 38, 0.08);
    }

    .storm-card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 3px;
    }

    .storm-title-name {
      font-family: var(--font-display);
      font-size: 14px;
      font-weight: 700;
      color: var(--text-pure);
    }

    .storm-intensity-tag {
      font-size: 11px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 3px;
    }
    .tag-severe { background: rgba(220, 38, 38, 0.2); color: #fca5a5; }
    .tag-elevated { background: rgba(217, 119, 6, 0.2); color: #fde047; }

    .storm-desc-line {
      font-size: 11.5px;
      color: var(--text-secondary);
    }

    /* ==========================================================================
       5. CENTER HERO: OPENSTREETMAP FOUNDATION (~70% VIEWPORT)
       ========================================================================== */
    .map-hero-wrapper {
      flex: 1;
      height: 100%;
      position: relative;
      background: #11141c;
    }

    #osmGeospatialMap {
      width: 100%;
      height: 100%;
      background: #11141c;
    }

    /* AIRNET-LEVEL CARTOGRAPHIC FILTER ON OSM TILES */
    /* Transforms standard OSM into deep, high-contrast cartographic dark basemap */
    .leaflet-tile-pane {
      filter: brightness(0.62) invert(1) contrast(1.18) hue-rotate(200deg) saturate(0.35);
    }

    /* FLOATING MINI MAP SEARCH (TOP-RIGHT WITH SAFE MARGIN) */
    .mini-map-search {
      position: absolute;
      top: 16px;
      right: 24px;
      z-index: 1000;
      width: 270px;
    }

    .search-input-wrap {
      position: relative;
      width: 100%;
    }

    .search-box-input {
      width: 100%;
      background: rgba(19, 23, 32, 0.94);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-medium);
      border-radius: 6px;
      padding: 8px 12px 8px 34px;
      color: var(--text-pure);
      font-family: var(--font-body);
      font-size: 12px;
      outline: none;
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.6);
      transition: all 0.15s ease;
    }
    .search-box-input:focus {
      border-color: rgba(255, 255, 255, 0.35);
      background: rgba(26, 31, 44, 0.98);
    }
    .search-box-input::placeholder {
      color: var(--text-muted);
    }

    .search-glyph-icon {
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      width: 15px;
      height: 15px;
      stroke: var(--text-muted);
      fill: none;
      stroke-width: 2;
      pointer-events: none;
    }

    .search-results-dropdown {
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      margin-top: 5px;
      background: var(--bg-panel-elevated);
      border: 1px solid var(--border-medium);
      border-radius: 6px;
      max-height: 220px;
      overflow-y: auto;
      display: none;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.8);
      z-index: 2000;
    }

    .search-result-row {
      padding: 8px 12px;
      font-size: 11.5px;
      color: var(--text-primary);
      border-bottom: 1px solid var(--border-subtle);
      cursor: pointer;
      line-height: 1.35;
    }
    .search-result-row:hover {
      background: var(--bg-panel-hover);
      color: var(--text-pure);
    }

    /* OBSERVED / NOWCAST REFINED SEGMENTED CONTROL */
    .segmented-mode-control {
      position: absolute;
      top: 16px;
      left: 18px;
      z-index: 1000;
      background: rgba(19, 23, 32, 0.94);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-medium);
      border-radius: 6px;
      padding: 3px;
      display: flex;
      gap: 3px;
      box-shadow: 0 4px 18px rgba(0,0,0,0.6);
    }

    .segmented-btn {
      background: none;
      border: none;
      color: var(--text-muted);
      font-family: var(--font-display);
      font-size: 11.5px;
      font-weight: 600;
      padding: 5px 12px;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .segmented-btn:hover { color: var(--text-warm-white); }
    .segmented-btn.active {
      background: #2a3242;
      color: var(--text-pure);
      font-weight: 700;
    }

    /* IMPACT LENS TOGGLE (WARM GOLD TREATMENT) */
    .btn-impact-lens-floating {
      position: absolute;
      top: 16px;
      left: 200px;
      z-index: 1000;
      background: rgba(19, 23, 32, 0.94);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-medium);
      border-radius: 6px;
      padding: 7px 14px;
      color: var(--text-secondary);
      font-family: var(--font-display);
      font-size: 11.5px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
      box-shadow: 0 4px 18px rgba(0,0,0,0.6);
      transition: all 0.15s ease;
    }
    .btn-impact-lens-floating:hover {
      color: var(--text-pure);
      border-color: rgba(255,255,255,0.25);
    }
    .btn-impact-lens-floating.active {
      background: rgba(217, 119, 6, 0.15);
      border-color: #d97706;
      color: #fde047;
    }

    /* RADAR REFLECTIVITY CARTOGRAPHIC LEGEND */
    .map-reflectivity-legend {
      position: absolute;
      bottom: 84px;
      right: 24px;
      z-index: 1000;
      background: rgba(19, 23, 32, 0.92);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 8px 12px;
      display: flex;
      flex-direction: column;
      gap: 4px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.6);
    }

    .legend-header-line {
      display: flex;
      justify-content: space-between;
      font-size: 10px;
      font-weight: 700;
      color: var(--text-secondary);
      text-transform: uppercase;
      letter-spacing: 0.4px;
    }

    .legend-ramp-spectrum {
      width: 190px;
      height: 6px;
      border-radius: 3px;
      background: linear-gradient(to right,
        #0284c7 0%,
        #10b981 30%,
        #eab308 55%,
        #f97316 75%,
        #dc2626 90%,
        #9333ea 100%
      );
    }

    .legend-scale-labels {
      display: flex;
      justify-content: space-between;
      font-size: 9px;
      color: var(--text-muted);
    }

    /* ==========================================================================
       6. FORECAST TIMELINE CONTROL (AIRNET MAP INSTRUMENT)
       ========================================================================== */
    .timeline-instrument-deck {
      position: absolute;
      bottom: 20px;
      left: 24px;
      right: 24px;
      z-index: 1000;
      background: rgba(19, 23, 32, 0.94);
      backdrop-filter: blur(14px);
      border: 1px solid var(--border-medium);
      border-radius: 10px;
      padding: 12px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 20px;
      box-shadow: 0 10px 32px rgba(0, 0, 0, 0.7);
    }

    .btn-timeline-play {
      background: #2a3242;
      border: 1px solid var(--border-medium);
      border-radius: 6px;
      padding: 7px 16px;
      color: var(--text-pure);
      font-family: var(--font-display);
      font-size: 12.5px;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 7px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .btn-timeline-play:hover {
      background: #353f54;
      border-color: rgba(255, 255, 255, 0.3);
    }

    .timeline-track-rail {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: relative;
    }

    .rail-connecting-bar {
      position: absolute;
      left: 12px;
      right: 12px;
      height: 3px;
      background: rgba(255, 255, 255, 0.12);
      border-radius: 2px;
      z-index: 1;
    }

    .timeline-node-item {
      position: relative;
      z-index: 2;
      display: flex;
      flex-direction: column;
      align-items: center;
      cursor: pointer;
      padding: 4px 10px;
      border-radius: 6px;
      transition: all 0.15s ease;
    }
    .timeline-node-item:hover {
      background: rgba(255, 255, 255, 0.06);
    }

    .node-center-dot {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: #2b3345;
      border: 2px solid var(--bg-panel);
      margin-bottom: 5px;
      transition: all 0.15s ease;
    }

    .node-text-label {
      font-family: var(--font-display);
      font-size: 11.5px;
      font-weight: 600;
      color: var(--text-muted);
    }

    .timeline-node-item.active .node-center-dot {
      background: #f3f4f6;
      border-color: #d97706;
      box-shadow: 0 0 8px rgba(217, 119, 6, 0.8);
      transform: scale(1.3);
    }
    .timeline-node-item.active .node-text-label {
      color: var(--text-pure);
      font-weight: 700;
    }

    /* ==========================================================================
       7. RIGHT PANEL: EDITORIAL CONTEXTUAL INTELLIGENCE
       ========================================================================== */
    .right-intel-column {
      width: 380px;
      min-width: 380px;
      background: var(--bg-panel);
      border-left: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      gap: 18px;
      padding: 20px;
      z-index: 500;
      overflow-y: auto;
    }

    /* Storm Header */
    .cell-editorial-header {
      display: flex;
      flex-direction: column;
      gap: 5px;
      border-bottom: 1px solid var(--border-subtle);
      padding-bottom: 14px;
    }

    .cell-title-line {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .cell-primary-title {
      font-family: var(--font-display);
      font-size: 24px;
      font-weight: 800;
      letter-spacing: -0.4px;
      color: var(--text-pure);
    }

    .cell-severity-pill {
      font-family: var(--font-display);
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      background: rgba(220, 38, 38, 0.18);
      border: 1px solid rgba(220, 38, 38, 0.4);
      color: #f87171;
      text-transform: uppercase;
    }

    .cell-narrative-sub {
      font-size: 13.5px;
      font-weight: 600;
      color: #fca5a5;
    }

    /* 4 Primary Hero Numbers (Clean 2x2 Grid) */
    .metrics-editorial-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }

    .metric-data-card {
      background: var(--bg-panel-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
    }

    .metric-hero-val {
      font-family: var(--font-display);
      font-size: 26px;
      font-weight: 800;
      color: var(--text-pure);
      line-height: 1.1;
      letter-spacing: -0.4px;
    }
    .metric-hero-val.val-severe { color: var(--vermilion-severe); }
    .metric-hero-val.val-highlight { color: #f3f4f6; }

    .metric-sub-label {
      font-size: 11.5px;
      color: var(--text-secondary);
      font-weight: 500;
      margin-top: 3px;
    }

    /* Section: STORM EVOLUTION NARRATIVE */
    .intel-section-box {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .intel-section-title {
      font-family: var(--font-display);
      font-size: 11.5px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
    }

    .evolution-steps-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
      border-left: 2px solid rgba(255, 255, 255, 0.1);
      margin-left: 6px;
      padding-left: 12px;
    }

    .evolution-step-item {
      display: flex;
      flex-direction: column;
      position: relative;
    }
    .evolution-step-item::before {
      content: "";
      position: absolute;
      left: -17px;
      top: 4px;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #4b5563;
      border: 2px solid var(--bg-panel);
    }
    .evolution-step-item.done::before {
      background: #10b981;
    }
    .evolution-step-item.active-now::before {
      background: var(--vermilion-severe);
      box-shadow: 0 0 6px var(--vermilion-severe);
    }

    .evo-timestamp {
      font-size: 10.5px;
      font-weight: 700;
      color: var(--text-muted);
    }
    .evo-description {
      font-size: 12px;
      font-weight: 500;
      color: var(--text-primary);
    }

    /* Section: WHAT CHANGED? */
    .delta-metrics-row {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
    }

    .delta-metric-card {
      background: var(--bg-panel-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 9px 11px;
      display: flex;
      flex-direction: column;
    }
    .delta-key {
      font-size: 11px;
      color: var(--text-secondary);
    }
    .delta-val {
      font-family: var(--font-display);
      font-size: 15px;
      font-weight: 800;
      color: var(--vermilion-severe);
      margin-top: 1px;
    }

    /* Section: POTENTIAL IMPACT INTERSECTIONS */
    .impact-targets-stack {
      display: flex;
      flex-direction: column;
      gap: 7px;
    }

    .impact-target-row {
      background: var(--bg-panel-elevated);
      border-left: 3px solid #d97706;
      border-radius: 0 6px 6px 0;
      padding: 9px 12px;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .impact-title-row {
      font-size: 12.5px;
      font-weight: 700;
      color: var(--text-pure);
      display: flex;
      justify-content: space-between;
    }

    .impact-desc-text {
      font-size: 11.5px;
      color: var(--text-secondary);
      line-height: 1.35;
    }

    /* ==========================================================================
       8. SCIENTIFIC METEOROLOGICAL MARKERS (MAP NATIVE)
       ========================================================================== */
    .leaflet-container {
      background: #11141c !important;
      font-family: var(--font-body);
    }

    /* Scientific Storm Cell Centroid Ring */
    .scientific-storm-ring {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      border: 2px solid #dc2626;
      background: rgba(220, 38, 38, 0.35);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #ffffff;
      font-family: var(--font-display);
      font-size: 11px;
      font-weight: 800;
      box-shadow: 0 0 16px rgba(220, 38, 38, 0.7);
      cursor: pointer;
    }

    /* Lightning Strike Discharge Point */
    .scientific-lightning-stroke {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #fde047;
      box-shadow: 0 0 10px #fde047;
      animation: lt-stroke-flash 1.6s infinite ease-out;
    }
    @keyframes lt-stroke-flash {
      0% { transform: scale(0.3); opacity: 1; }
      50% { transform: scale(2.2); opacity: 0.6; }
      100% { transform: scale(3.4); opacity: 0; }
    }

    /* Clean Map City Marker */
    .carto-city-label {
      background: rgba(14, 17, 23, 0.88);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 3px;
      padding: 2px 6px;
      font-size: 11px;
      font-weight: 600;
      color: #f3f4f6;
      white-space: nowrap;
      pointer-events: none;
    }

    /* Search Location Marker Pin */
    .search-pin-marker {
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: #3b82f6;
      border: 2px solid #ffffff;
      box-shadow: 0 0 12px #3b82f6;
    }
  </style>
</head>
<body>

  <!-- ==========================================================================
       TOP PRODUCT HEADER
       ========================================================================== -->
  <header class="top-header">
    <div class="brand-group">
      <div class="brand-mark-box">
        <!-- Professional Radar Sweep Glyph -->
        <svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8zm0-14a6 6 0 0 0-6 6h6z"/></svg>
      </div>
      <div class="brand-text-wrap">
        <span class="brand-title">VAJRA</span>
        <span class="brand-subtitle">Very-short-term Atmospheric Risk &amp; Joint Analysis</span>
      </div>
    </div>

    <!-- Center: Regional Atmospheric Overview -->
    <div class="regional-status-bar">
      <div class="domain-indicator">
        <span class="live-pulse-dot"></span>
        <span>EASTERN INDIA</span>
      </div>
      <div class="domain-divider" style="width:1px; height:16px; background:var(--border-subtle);"></div>
      <div class="domain-stats-summary">
        <strong>12</strong> Active Storms &bull; <strong>4</strong> Intensifying &bull; <strong>1</strong> High-Impact Corridor
      </div>
    </div>

    <!-- Right Header Tools -->
    <div class="header-right-tools">
      <div class="domain-stats-summary" style="font-size:12px;">
        <span>Horizon:</span>
        <strong id="topHorizonLabel">Nowcast to +30m</strong>
      </div>
      <button class="btn-header-ghost active" id="btnFocusStorm">
        <!-- Target / Crosshair Glyph -->
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M22 12h-4M6 12H2M12 6V2M12 22v-4"/></svg>
        <span>FOCUS CELL 024</span>
      </button>
    </div>
  </header>

  <!-- ==========================================================================
       MAIN APP WORKSPACE
       ========================================================================== -->
  <main class="app-workspace">

    <!-- LEFT PANEL: CONTROLS, LAYERS & ACTIVE STORMS -->
    <aside class="left-controls-rail">
      <!-- Forecast Horizon Selector -->
      <div>
        <div class="rail-section-label">
          <span>FORECAST HORIZON</span>
          <span style="color:#d97706; font-weight:700;" id="horizonIndicator">+30 MIN</span>
        </div>
        <div class="horizon-selector-grid">
          <button class="horizon-pill-btn" data-step="1">15 MIN</button>
          <button class="horizon-pill-btn active" data-step="2">30 MIN</button>
          <button class="horizon-pill-btn" data-step="3">45 MIN</button>
          <button class="horizon-pill-btn" data-step="4">1 HR</button>
          <button class="horizon-pill-btn" data-step="5">2 HR</button>
          <button class="horizon-pill-btn" data-step="6">3 HR</button>
        </div>
      </div>

      <!-- Atmospheric Layers with Scientific Icons -->
      <div>
        <div class="rail-section-label">
          <span>ATMOSPHERIC LAYERS</span>
        </div>
        <div class="layer-cards-stack">
          <!-- Radar -->
          <div class="layer-row-card active" id="layerToggleRadar">
            <div class="layer-left-info">
              <div class="layer-glyph-box">
                <svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 14a4 4 0 1 1 4-4 4 4 0 0 1-4 4zm0-10a6 6 0 0 0-6 6h6z"/></svg>
              </div>
              <div>
                <div class="layer-title-text">Radar Reflectivity</div>
                <div class="layer-meta-text">Composite dBZ &bull; LIVE</div>
              </div>
            </div>
            <div class="layer-toggle-switch"></div>
          </div>

          <!-- Satellite -->
          <div class="layer-row-card active" id="layerToggleSat">
            <div class="layer-left-info">
              <div class="layer-glyph-box">
                <svg viewBox="0 0 24 24"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" stroke-width="1.8"/></svg>
              </div>
              <div>
                <div class="layer-title-text">Satellite Cloud Top</div>
                <div class="layer-meta-text">INSAT-3DR 10.8µm &bull; 8m ago</div>
              </div>
            </div>
            <div class="layer-toggle-switch"></div>
          </div>

          <!-- Lightning -->
          <div class="layer-row-card active" id="layerToggleLtg">
            <div class="layer-left-info">
              <div class="layer-glyph-box">
                <svg viewBox="0 0 24 24"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" stroke-width="1.8"/></svg>
              </div>
              <div>
                <div class="layer-title-text">Lightning Discharges</div>
                <div class="layer-meta-text">Real-time pulses &bull; LIVE</div>
              </div>
            </div>
            <div class="layer-toggle-switch"></div>
          </div>

          <!-- Storm Trajectories -->
          <div class="layer-row-card active" id="layerToggleTracks">
            <div class="layer-left-info">
              <div class="layer-glyph-box">
                <svg viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
              </div>
              <div>
                <div class="layer-title-text">Storm Trajectories</div>
                <div class="layer-meta-text">Forecast Shadow &bull; ACTIVE</div>
              </div>
            </div>
            <div class="layer-toggle-switch"></div>
          </div>
        </div>
      </div>

      <!-- Tracked Storms Stack -->
      <div style="flex:1;">
        <div class="rail-section-label">
          <span>TRACKED STORMS</span>
          <span style="color:var(--vermilion-severe);">3 DETECTED</span>
        </div>
        <div class="storms-list-stack">
          <!-- Storm Cell 024 -->
          <div class="storm-select-card selected" id="stormCard024" onclick="selectStormCell('024')">
            <div class="storm-card-header">
              <span class="storm-title-name">Storm Cell 024</span>
              <span class="storm-intensity-tag tag-severe">68 dBZ</span>
            </div>
            <div class="storm-desc-line">Rapidly intensifying &bull; ENE 34 km/h</div>
          </div>

          <!-- Storm Cell 018 -->
          <div class="storm-select-card" id="stormCard018" onclick="selectStormCell('018')">
            <div class="storm-card-header">
              <span class="storm-title-name">Storm Cell 018</span>
              <span class="storm-intensity-tag tag-elevated">52 dBZ</span>
            </div>
            <div class="storm-desc-line">Forward advection &bull; E 28 km/h</div>
          </div>

          <!-- Storm Cell 031 -->
          <div class="storm-select-card" id="stormCard031" onclick="selectStormCell('031')">
            <div class="storm-card-header">
              <span class="storm-title-name">Storm Cell 031</span>
              <span class="storm-intensity-tag tag-severe">59 dBZ</span>
            </div>
            <div class="storm-desc-line">Coastal squall segment &bull; NE 52 km/h</div>
          </div>
        </div>
      </div>
    </aside>

    <!-- CENTER HERO: REAL OPENSTREETMAP FOUNDATION (~70% VIEWPORT) -->
    <section class="map-hero-wrapper">
      <div id="osmGeospatialMap"></div>

      <!-- OBSERVED / NOWCAST REFINED SEGMENTED CONTROL -->
      <div class="segmented-mode-control">
        <button class="segmented-btn" id="btnModeObserved">OBSERVED</button>
        <button class="segmented-btn active" id="btnModeNowcast">NOWCAST</button>
      </div>

      <!-- IMPACT LENS TOGGLE -->
      <button class="btn-impact-lens-floating" id="btnToggleImpactLens">
        <!-- Layers / Intersection Glyph -->
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
        <span>IMPACT LENS</span>
      </button>

      <!-- FLOATING MINI MAP SEARCH (TOP-RIGHT WITH SAFE MARGIN) -->
      <div class="mini-map-search">
        <div class="search-input-wrap">
          <svg class="search-glyph-icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
          <input type="text" class="search-box-input" id="osmMiniSearch" placeholder="Search city, district or location..." autocomplete="off" />
          <div class="search-results-dropdown" id="searchResultsDropdown"></div>
        </div>
      </div>

      <!-- RADAR REFLECTIVITY LEGEND -->
      <div class="map-reflectivity-legend">
        <div class="legend-header-line">
          <span>Reflectivity (dBZ)</span>
          <span style="color:var(--vermilion-severe);">Hail &gt; 55</span>
        </div>
        <div class="legend-ramp-spectrum"></div>
        <div class="legend-scale-labels">
          <span>20</span>
          <span>35</span>
          <span>45</span>
          <span>55</span>
          <span>65+</span>
        </div>
      </div>

      <!-- FORECAST TIMELINE CONTROL -->
      <div class="timeline-instrument-deck">
        <button class="btn-timeline-play" id="btnPlayForecast">
          <span id="playIcon">▶</span>
          <span id="playLabel">PLAY EVOLUTION</span>
        </button>

        <div class="timeline-track-rail">
          <div class="rail-connecting-bar"></div>

          <div class="timeline-node-item" data-idx="0">
            <div class="node-center-dot"></div>
            <span class="node-text-label">NOW</span>
          </div>

          <div class="timeline-node-item" data-idx="1">
            <div class="node-center-dot"></div>
            <span class="node-text-label">+15m</span>
          </div>

          <div class="timeline-node-item active" data-idx="2">
            <div class="node-center-dot"></div>
            <span class="node-text-label">+30m</span>
          </div>

          <div class="timeline-node-item" data-idx="3">
            <div class="node-center-dot"></div>
            <span class="node-text-label">+45m</span>
          </div>

          <div class="timeline-node-item" data-idx="4">
            <div class="node-center-dot"></div>
            <span class="node-text-label">+60m</span>
          </div>

          <div class="timeline-node-item" data-idx="5">
            <div class="node-center-dot"></div>
            <span class="node-text-label">+90m</span>
          </div>

          <div class="timeline-node-item" data-idx="6">
            <div class="node-center-dot"></div>
            <span class="node-text-label">+120m</span>
          </div>
        </div>
      </div>
    </section>

    <!-- RIGHT PANEL: EDITORIAL CONTEXTUAL INTELLIGENCE -->
    <aside class="right-intel-column">
      <!-- Cell Editorial Header -->
      <div class="cell-editorial-header">
        <div class="cell-title-line">
          <span class="cell-primary-title" id="intelStormId">STORM CELL 024</span>
          <span class="cell-severity-pill" id="intelSeverityBadge">SEVERE</span>
        </div>
        <div class="cell-narrative-sub" id="intelNarrativeSub">RAPIDLY INTENSIFYING</div>
      </div>

      <!-- 4 Primary Hero Numbers -->
      <div class="metrics-editorial-grid">
        <div class="metric-data-card">
          <span class="metric-hero-val val-severe" id="intelDbzVal">68 dBZ</span>
          <span class="metric-sub-label">Current intensity</span>
        </div>

        <div class="metric-data-card">
          <span class="metric-hero-val" id="intelSpeedVal">34 km/h</span>
          <span class="metric-sub-label" id="intelDirVal">SOUTHEAST</span>
        </div>

        <div class="metric-data-card">
          <span class="metric-hero-val val-highlight" id="intelArrivalVal">18–27 min</span>
          <span class="metric-sub-label">Arrival window</span>
        </div>

        <div class="metric-data-card">
          <span class="metric-hero-val" id="intelConfidenceVal">87%</span>
          <span class="metric-sub-label">Forecast confidence</span>
        </div>
      </div>

      <!-- Section: STORM EVOLUTION NARRATIVE -->
      <div class="intel-section-box">
        <div class="intel-section-title">
          <span>STORM EVOLUTION</span>
          <span style="color:#d97706;">5 PHASES</span>
        </div>
        <div class="evolution-steps-list" id="evolutionStepsContainer">
          <div class="evolution-step-item done">
            <span class="evo-timestamp">14:10 &bull; FORMED</span>
            <span class="evo-description">Cell initiated in Midnapore sector (38 dBZ)</span>
          </div>
          <div class="evolution-step-item done">
            <span class="evo-timestamp">14:18 &bull; DEVELOPING</span>
            <span class="evo-description">Reflectivity surge (+10 dBZ in 8 min)</span>
          </div>
          <div class="evolution-step-item done">
            <span class="evo-timestamp">14:26 &bull; LIGHTNING ACCELERATION</span>
            <span class="evo-description">Discharge rate spiked to 38 strokes/min</span>
          </div>
          <div class="evolution-step-item active-now">
            <span class="evo-timestamp">14:34 &bull; INTENSIFYING (NOW)</span>
            <span class="evo-description">Severe hail core with overshooting convective top</span>
          </div>
          <div class="evolution-step-item">
            <span class="evo-timestamp">14:50 &bull; PROJECTED PEAK</span>
            <span class="evo-description">Direct crossing of Kolkata-Howrah urban corridor</span>
          </div>
        </div>
      </div>

      <!-- Section: WHAT CHANGED? · LAST 15 MIN -->
      <div class="intel-section-box">
        <div class="intel-section-title">
          <span>WHAT CHANGED? &bull; LAST 15 MIN</span>
          <span style="color:var(--vermilion-severe);">↗ ESCALATING</span>
        </div>
        <div class="delta-metrics-row">
          <div class="delta-metric-card">
            <span class="delta-key">Radar growth</span>
            <span class="delta-val">+14 dBZ</span>
          </div>
          <div class="delta-metric-card">
            <span class="delta-key">Lightning activity</span>
            <span class="delta-val">+27%</span>
          </div>
          <div class="delta-metric-card">
            <span class="delta-key">Cloud-top cooling</span>
            <span class="delta-val" style="color:#38bdf8;">&darr; -6.2&deg;C</span>
          </div>
          <div class="delta-metric-card">
            <span class="delta-key">Storm area</span>
            <span class="delta-val">+18%</span>
          </div>
        </div>
      </div>

      <!-- Section: POTENTIAL IMPACT INTERSECTIONS -->
      <div class="intel-section-box">
        <div class="intel-section-title">
          <span>POTENTIAL IMPACT &bull; CORRIDOR</span>
          <span style="color:#d97706;">INTERSECTION</span>
        </div>
        <div class="impact-targets-stack">
          <div class="impact-target-row">
            <div class="impact-title-row">
              <span>✈ VECC Kolkata Airport</span>
              <span style="color:var(--vermilion-severe);">ETA 22 min</span>
            </div>
            <span class="impact-desc-text">Runway 19L/01R microburst risk. Holding advisory active.</span>
          </div>

          <div class="impact-target-row">
            <div class="impact-title-row">
              <span>🛣 Major Highways NH-16 &amp; NH-19</span>
              <span style="color:#d97706;">ETA 14 min</span>
            </div>
            <span class="impact-desc-text">Direct squall crossing with crosswinds exceeding 75 km/h.</span>
          </div>

          <div class="impact-target-row">
            <div class="impact-title-row">
              <span>⚡ 765kV Regional Substation</span>
              <span style="color:#f97316;">High Risk</span>
            </div>
            <span class="impact-desc-text">High-density CG lightning strike cluster in Midnapore sector.</span>
          </div>

          <div class="impact-target-row">
            <div class="impact-title-row">
              <span>👥 Population Settlements</span>
              <span style="color:#ffffff;">182K Persons</span>
            </div>
            <span class="impact-desc-text">High-density urban wards exposed in Howrah and Hooghly districts.</span>
          </div>
        </div>
      </div>
    </aside>
  </main>

  <!-- ==========================================================================
       JAVASCRIPT: SCIENTIFIC CARTOGRAPHY & INTERACTION
       ========================================================================== -->
  <script>
    /* ==========================================================================
       1. DATA DEFINITIONS & STORM CATALOG
       ========================================================================== */
    const STORM_CATALOG = {
      '024': {
        id: 'STORM CELL 024',
        badge: 'SEVERE',
        narrative: 'RAPIDLY INTENSIFYING',
        dbz: '68 dBZ',
        speed: '34 km/h',
        direction: 'SOUTHEAST',
        arrival: '18–27 min',
        confidence: '87%',
        center: [22.60, 88.20],
        track: [
          [22.42, 87.85], // NOW
          [22.51, 88.08], // +15m
          [22.60, 88.32], // +30m
          [22.68, 88.54], // +45m
          [22.76, 88.76], // +60m
          [22.88, 89.10], // +90m
          [23.00, 89.45]  // +120m
        ],
        lightnings: [
          [22.44, 87.87], [22.41, 87.82], [22.47, 87.92],
          [22.39, 87.80], [22.45, 87.94]
        ],
        story: [
          { time: '14:10 \u2022 FORMED', desc: 'Cell initiated in Midnapore sector (38 dBZ)', status: 'done' },
          { time: '14:18 \u2022 DEVELOPING', desc: 'Reflectivity surge (+10 dBZ in 8 min)', status: 'done' },
          { time: '14:26 \u2022 LIGHTNING ACCELERATION', desc: 'Discharge rate spiked to 38 strokes/min', status: 'done' },
          { time: '14:34 \u2022 INTENSIFYING (NOW)', desc: 'Severe hail core with overshooting convective top', status: 'active-now' },
          { time: '14:50 \u2022 PROJECTED PEAK', desc: 'Direct crossing of Kolkata-Howrah urban corridor', status: 'pending' }
        ]
      },
      '018': {
        id: 'STORM CELL 018',
        badge: 'ELEVATED',
        narrative: 'FORWARD ADVECTION',
        dbz: '52 dBZ',
        speed: '28 km/h',
        direction: 'EAST',
        arrival: '35–45 min',
        confidence: '82%',
        center: [23.25, 88.10],
        track: [
          [23.24, 87.88], [23.28, 88.14], [23.32, 88.38],
          [23.36, 88.62], [23.40, 88.86], [23.46, 89.18], [23.52, 89.50]
        ],
        lightnings: [
          [23.22, 87.85], [23.26, 87.91], [23.25, 87.89]
        ],
        story: [
          { time: '13:55 \u2022 FORMED', desc: 'Burdwan convective initiation', status: 'done' },
          { time: '14:15 \u2022 DEVELOPING', desc: 'Cluster consolidating eastwards', status: 'done' },
          { time: '14:34 \u2022 ADVECTION (NOW)', desc: 'Steady moderate precipitation band', status: 'active-now' },
          { time: '15:10 \u2022 PASSAGE', desc: 'Passing Ranaghat railway hub', status: 'pending' }
        ]
      },
      '031': {
        id: 'STORM CELL 031',
        badge: 'SEVERE',
        narrative: 'COASTAL SQUALL SEGMENT',
        dbz: '59 dBZ',
        speed: '52 km/h',
        direction: 'NORTHEAST',
        arrival: '16–24 min',
        confidence: '89%',
        center: [21.80, 87.35],
        track: [
          [21.65, 87.05], [21.80, 87.30], [21.95, 87.55],
          [22.10, 87.80], [22.25, 88.05], [22.45, 88.40], [22.65, 88.75]
        ],
        lightnings: [
          [21.68, 87.10], [21.62, 87.02], [21.72, 87.18]
        ],
        story: [
          { time: '14:00 \u2022 FORMED', desc: 'Balasore coastal squall initiation', status: 'done' },
          { time: '14:20 \u2022 BOWING', desc: 'Bow echo segment developing with gust front', status: 'done' },
          { time: '14:34 \u2022 SEVERE (NOW)', desc: 'Approaching Digha coastal defense line', status: 'active-now' },
          { time: '15:00 \u2022 INDUSTRIAL PASSAGE', desc: 'Haldia port & petrochem industrial zone', status: 'pending' }
        ]
      }
    };

    let activeStormId = '024';
    let currentStep = 2; // +30m
    let currentMode = 'nowcast'; // 'observed' or 'nowcast'
    let isImpactLensActive = false;
    let isPlaying = false;
    let playInterval = null;

    let map = null;
    let layerRadar = null;
    let layerSat = null;
    let layerLtg = null;
    let layerTracks = null;
    let layerImpact = null;
    let layerSearchPin = null;

    /* ==========================================================================
       2. INITIALIZATION
       ========================================================================== */
    window.addEventListener('DOMContentLoaded', () => {
      initMapEngine();
      setupInteractions();
      renderAtmosphericLayers();
    });

    /* ==========================================================================
       3. MAP INITIALIZATION (TRUE OPENSTREETMAP CARTOGRAPHY)
       ========================================================================== */
    function initMapEngine() {
      // Create Leaflet map centered over Eastern India
      map = L.map('osmGeospatialMap', {
        zoomControl: false,
        attributionControl: false,
        preferCanvas: true
      }).setView([22.65, 88.25], 8);

      L.control.zoom({ position: 'bottomleft' }).addTo(map);

      // OpenStreetMap Tiles with Dark Inverted Cartographic Styling
      // Zero API key required, high definition roads, borders, water and labels
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        opacity: 0.95
      }).addTo(map);

      // Map Layer Groups
      layerRadar = L.layerGroup().addTo(map);
      layerSat = L.layerGroup().addTo(map);
      layerLtg = L.layerGroup().addTo(map);
      layerTracks = L.layerGroup().addTo(map);
      layerImpact = L.layerGroup().addTo(map);
      layerSearchPin = L.layerGroup().addTo(map);

      // Add Cartographic City Geotags
      const cities = [
        { name: "Kolkata", lat: 22.5726, lon: 88.3639 },
        { name: "Howrah", lat: 22.5958, lon: 88.2636 },
        { name: "Kharagpur", lat: 22.3460, lon: 87.2320 },
        { name: "Burdwan", lat: 23.2324, lon: 87.8615 },
        { name: "Midnapore", lat: 22.4257, lon: 87.3199 },
        { name: "Durgapur", lat: 23.5204, lon: 87.3119 },
        { name: "Balasore", lat: 21.4934, lon: 86.9135 },
        { name: "Haldia", lat: 22.0667, lon: 88.0698 }
      ];

      cities.forEach(c => {
        const badge = L.divIcon({
          className: 'city-tag-wrap',
          html: `<div class="carto-city-label">${c.name}</div>`,
          iconSize: [60, 18],
          iconAnchor: [30, 9]
        });
        L.marker([c.lat, c.lon], { icon: badge, interactive: false }).addTo(map);
      });
    }

    /* ==========================================================================
       4. METEOROLOGICAL ATMOSPHERIC RENDERING (NATURAL CONTOURS)
       ========================================================================== */
    function renderAtmosphericLayers() {
      layerRadar.clearLayers();
      layerLtg.clearLayers();
      layerTracks.clearLayers();
      layerImpact.clearLayers();

      const storm = STORM_CATALOG[activeStormId];
      const track = storm.track;

      // 1. FORECAST UNCERTAINTY CONE (Soft feathered polygon)
      if (currentMode === 'nowcast') {
        const p0 = track[0];
        const pTarget = track[currentStep] || track[track.length - 1];
        const spread = 0.08 + (currentStep * 0.05);

        const uncertaintyCone = [
          [p0[0], p0[1]],
          [pTarget[0] + spread * 0.75, pTarget[1] - spread],
          [pTarget[0] + spread * 1.15, pTarget[1] + spread],
          [pTarget[0] - spread * 0.55, pTarget[1] + spread * 0.85],
          [p0[0], p0[1]]
        ];

        L.polygon(uncertaintyCone, {
          color: '#a855f7',
          fillColor: '#a855f7',
          fillOpacity: 0.12,
          weight: 1.5,
          dashArray: '4, 6'
        }).addTo(layerTracks);
      }

      // 2. STORM TRAJECTORY (Clean directional vector)
      L.polyline(track, {
        color: '#f59e0b',
        weight: 2.5,
        opacity: 0.85,
        dashArray: '5, 5'
      }).addTo(layerTracks);

      // 3. CURRENT STORM FOOTPRINT (Multi-contour radar reflectivity)
      const t0 = track[0];

      // Outer moderate rain (35 dBZ green)
      L.circle(t0, {
        radius: 22000,
        color: '#10b981',
        fillColor: '#10b981',
        fillOpacity: 0.28,
        weight: 1
      }).addTo(layerRadar);

      // Elevated convective core (50 dBZ amber/orange)
      L.circle(t0, {
        radius: 13000,
        color: '#f97316',
        fillColor: '#f97316',
        fillOpacity: 0.5,
        weight: 1.5
      }).addTo(layerRadar);

      // Severe Hail Core (65+ dBZ vermilion/red)
      L.circle(t0, {
        radius: 6500,
        color: '#dc2626',
        fillColor: '#dc2626',
        fillOpacity: 0.8,
        weight: 2
      }).addTo(layerRadar);

      // 4. STORM SHADOWS (Progressively translucent future footprints fading downwind)
      if (currentMode === 'nowcast') {
        const stepLabels = ['NOW', '+15m', '+30m', '+45m', '+60m', '+90m', '+120m'];

        for (let i = 1; i <= currentStep; i++) {
          const pt = track[i];
          if (!pt) continue;

          // Progressive translucency decay
          const opacity = Math.max(0.12, 0.46 - (i * 0.07));
          const shadowRadius = 18000 + (i * 2200);

          L.circle(pt, {
            radius: shadowRadius,
            color: '#f97316',
            fillColor: '#f97316',
            fillOpacity: opacity,
            weight: 1,
            dashArray: '3, 4'
          }).addTo(layerRadar);

          // Trajectory Waypoint node
          L.circleMarker(pt, {
            radius: 5,
            color: '#f59e0b',
            fillColor: '#11141c',
            fillOpacity: 1,
            weight: 2
          }).bindTooltip(`${stepLabels[i]} position (${storm.id})`, { permanent: false }).addTo(layerTracks);
        }
      }

      // 5. ACTIVE STORM CELL SCIENTIFIC CENTROID
      const activeCentroid = (currentMode === 'nowcast' && currentStep > 0) ? track[currentStep] : t0;
      const coreIcon = L.divIcon({
        className: 'storm-ring-wrap',
        html: `<div class="scientific-storm-ring" title="${storm.id}">${parseInt(storm.dbz)}</div>`,
        iconSize: [36, 36],
        iconAnchor: [18, 18]
      });
      L.marker(activeCentroid, { icon: coreIcon }).addTo(layerTracks);

      // 6. SCIENTIFIC LIGHTNING DISCHARGES (Electric stroke clusters)
      storm.lightnings.forEach(lt => {
        const ltIcon = L.divIcon({
          className: 'lt-stroke-wrap',
          html: '<div class="scientific-lightning-stroke"></div>',
          iconSize: [12, 12],
          iconAnchor: [6, 6]
        });
        L.marker(lt, { icon: ltIcon }).addTo(layerLtg);
      });

      // 7. IMPACT LENS INTERSECTIONS
      if (isImpactLensActive) {
        const assets = [
          { name: "VECC Kolkata Airport", pt: [22.654, 88.446], desc: "Runway approach crossing in 22 min" },
          { name: "NH-16 & NH-19 Highway Hub", pt: [22.48, 87.95], desc: "Direct squall crossing (75 km/h gusts)" },
          { name: "765kV Regional Substation", pt: [22.42, 87.35], desc: "High CG lightning strike corridor" }
        ];

        assets.forEach(a => {
          L.circle(a.pt, {
            radius: 8000,
            color: '#d97706',
            fillColor: '#d97706',
            fillOpacity: 0.22,
            weight: 1.5
          }).addTo(layerImpact);

          L.circleMarker(a.pt, {
            radius: 6,
            color: '#d97706',
            fillColor: '#fde047',
            fillOpacity: 1,
            weight: 2
          }).bindPopup(`<strong>${a.name}</strong><br>${a.desc}`).addTo(layerImpact);
        });
      }
    }

    /* ==========================================================================
       5. SELECT STORM CELL (INTERACTION & EDITORIAL UPDATE)
       ========================================================================== */
    function selectStormCell(stormId) {
      activeStormId = stormId;
      const storm = STORM_CATALOG[stormId];

      // Update card selections
      document.querySelectorAll('.storm-select-card').forEach(c => c.classList.remove('selected'));
      const activeCard = document.getElementById(`stormCard${stormId}`);
      if (activeCard) activeCard.classList.add('selected');

      // Update Right Editorial Panel
      document.getElementById('intelStormId').textContent = storm.id;
      document.getElementById('intelSeverityBadge').textContent = storm.badge;
      document.getElementById('intelNarrativeSub').textContent = storm.narrative;

      document.getElementById('intelDbzVal').textContent = storm.dbz;
      document.getElementById('intelSpeedVal').textContent = storm.speed;
      document.getElementById('intelDirVal').textContent = storm.direction;
      document.getElementById('intelArrivalVal').textContent = storm.arrival;
      document.getElementById('intelConfidenceVal').textContent = storm.confidence;

      // Update Narrative Timeline
      const storyContainer = document.getElementById('evolutionStepsContainer');
      storyContainer.innerHTML = '';
      storm.story.forEach(step => {
        const item = document.createElement('div');
        item.className = `evolution-step-item ${step.status}`;
        item.innerHTML = `
          <span class="evo-timestamp">${step.time}</span>
          <span class="evo-description">${step.desc}</span>
        `;
        storyContainer.appendChild(item);
      });

      // Fly map to storm centroid
      map.flyTo(storm.center, 8, { duration: 0.8 });

      // Re-render atmospheric features
      renderAtmosphericLayers();
    }

    /* ==========================================================================
       6. TIMELINE SCRUBBER
       ========================================================================== */
    function setHorizonStep(stepIdx) {
      currentStep = stepIdx;

      // Update timeline nodes
      document.querySelectorAll('.timeline-node-item').forEach((node, i) => {
        node.classList.toggle('active', i === stepIdx);
      });

      // Update left buttons
      document.querySelectorAll('.horizon-pill-btn').forEach((btn, i) => {
        btn.classList.toggle('active', i === stepIdx);
      });

      const labels = ['NOW', '+15 MIN', '+30 MIN', '+45 MIN', '+60 MIN', '+90 MIN', '+120 MIN'];
      document.getElementById('horizonIndicator').textContent = labels[stepIdx];
      document.getElementById('topHorizonLabel').textContent = `Nowcast to ${labels[stepIdx]}`;

      renderAtmosphericLayers();
    }

    /* ==========================================================================
       7. MINI MAP SEARCH WITH NOMINATIM GEOCODING
       ========================================================================== */
    function setupSearchEngine() {
      const searchInput = document.getElementById('osmMiniSearch');
      const dropdown = document.getElementById('searchResultsDropdown');

      let debounceTimer = null;
      searchInput.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        const query = searchInput.value.trim();
        if (query.length < 2) {
          dropdown.style.display = 'none';
          return;
        }

        debounceTimer = setTimeout(async () => {
          try {
            // First query our backend /osm/search endpoint
            let data = null;
            try {
              const resp = await fetch(`/osm/search?q=${encodeURIComponent(query)}`);
              if (resp.ok) data = await resp.json();
            } catch(e) {}

            // Fallback directly to Nominatim if backend endpoint is unavailable
            if (!data || !data.results || data.results.length === 0) {
              const directResp = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=json&limit=5&countrycodes=in`);
              if (directResp.ok) {
                const raw = await directResp.json();
                data = { results: raw.map(r => ({ display_name: r.display_name, lat: parseFloat(r.lat), lon: parseFloat(r.lon) })) };
              }
            }

            if (data && data.results && data.results.length > 0) {
              dropdown.innerHTML = '';
              data.results.forEach(res => {
                const row = document.createElement('div');
                row.className = 'search-result-row';
                row.textContent = res.display_name;
                row.addEventListener('click', () => {
                  dropdown.style.display = 'none';
                  searchInput.value = res.display_name.split(',')[0];

                  // Fly map to searched coordinates
                  map.flyTo([res.lat, res.lon], 11, { duration: 1.2 });

                  // Place clean location pin marker
                  layerSearchPin.clearLayers();
                  const pinIcon = L.divIcon({
                    className: 'search-pin-wrap',
                    html: '<div class="search-pin-marker"></div>',
                    iconSize: [14, 14],
                    iconAnchor: [7, 7]
                  });
                  L.marker([res.lat, res.lon], { icon: pinIcon })
                    .bindPopup(`<strong>${res.display_name.split(',')[0]}</strong><br>${res.lat.toFixed(3)}° N, ${res.lon.toFixed(3)}° E`)
                    .addTo(layerSearchPin)
                    .openPopup();
                });
                dropdown.appendChild(row);
              });
              dropdown.style.display = 'block';
            } else {
              dropdown.style.display = 'none';
            }
          } catch(err) {
            dropdown.style.display = 'none';
          }
        }, 300);
      });

      document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
          dropdown.style.display = 'none';
        }
      });
    }

    /* ==========================================================================
       8. UI EVENT HANDLERS & MICRO-INTERACTIONS
       ========================================================================== */
    function setupInteractions() {
      setupSearchEngine();

      // Horizon Buttons
      document.querySelectorAll('.horizon-pill-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          setHorizonStep(parseInt(btn.dataset.step));
        });
      });

      // Timeline Nodes
      document.querySelectorAll('.timeline-node-item').forEach(node => {
        node.addEventListener('click', () => {
          setHorizonStep(parseInt(node.dataset.idx));
        });
      });

      // Play Evolution
      const playBtn = document.getElementById('btnPlayForecast');
      const playIcon = document.getElementById('playIcon');
      const playLabel = document.getElementById('playLabel');

      playBtn.addEventListener('click', () => {
        isPlaying = !isPlaying;
        if (isPlaying) {
          playIcon.textContent = '⏸';
          playLabel.textContent = 'PAUSE';
          playInterval = setInterval(() => {
            let next = (currentStep + 1) % 7;
            setHorizonStep(next);
          }, 1600);
        } else {
          playIcon.textContent = '▶';
          playLabel.textContent = 'PLAY EVOLUTION';
          clearInterval(playInterval);
        }
      });

      // Observed / Nowcast Segmented Buttons
      document.getElementById('btnModeObserved').addEventListener('click', () => {
        currentMode = 'observed';
        document.getElementById('btnModeObserved').classList.add('active');
        document.getElementById('btnModeNowcast').classList.remove('active');
        renderAtmosphericLayers();
      });

      document.getElementById('btnModeNowcast').addEventListener('click', () => {
        currentMode = 'nowcast';
        document.getElementById('btnModeNowcast').classList.add('active');
        document.getElementById('btnModeObserved').classList.remove('active');
        renderAtmosphericLayers();
      });

      // Impact Lens Toggle
      const impactBtn = document.getElementById('btnToggleImpactLens');
      impactBtn.addEventListener('click', () => {
        isImpactLensActive = !isImpactLensActive;
        impactBtn.classList.toggle('active', isImpactLensActive);
        renderAtmosphericLayers();
      });

      // Focus Storm Button
      document.getElementById('btnFocusStorm').addEventListener('click', () => {
        const storm = STORM_CATALOG[activeStormId];
        map.flyTo(storm.center, 9, { duration: 1.0 });
      });

      // Layer Toggles
      const bindToggle = (btnId, layer) => {
        const el = document.getElementById(btnId);
        el.addEventListener('click', () => {
          el.classList.toggle('active');
          if (el.classList.contains('active')) map.addLayer(layer);
          else map.removeLayer(layer);
        });
      };

      bindToggle('layerToggleRadar', layerRadar);
      bindToggle('layerToggleSat', layerSat);
      bindToggle('layerToggleLtg', layerLtg);
      bindToggle('layerToggleTracks', layerTracks);
    }
  </script>
</body>
</html>
"""

with open("dashboard/index.html", "w", encoding="utf-8") as f:
    f.write(html_code)

print(f"Generated AirNet-Grade VAJRA Dashboard: {len(html_code)} bytes")
