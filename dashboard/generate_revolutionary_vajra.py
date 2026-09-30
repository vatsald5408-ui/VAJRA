# -*- coding: utf-8 -*-
"""
VAJRA — UI/UX Spatial Revolution
A Living Atmospheric Canvas (Edge-to-Edge Fullscreen Environment)
- NO permanent left/right sidebars
- Edge-to-edge full viewport OSM cartography
- Floating Situation Bar at top (thin atmospheric status line)
- Floating Contextual Tool Dock (left edge, expandable)
- Emergent Contextual Storm Inspector (slides out from right when storm is selected)
- Storm Focus Mode (smooth zoom, non-selected dimming, spatial trajectory)
- Spatial Forecast Scrubber floating near bottom edge (OBSERVED ─── NOW ─── +15m ─── +120m)
- Field View presentation mode (hides all chrome for pure cinematic atmospheric exploration)
- Spatial "What Changed" delta tags near the storm on the map
- Pure OpenStreetMap cartography with AirNet-grade styling, zero emojis, professional SVG glyphs
"""

code = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>VAJRA — Atmospheric Intelligence Platform</title>
  <meta name="description" content="VAJRA: High-resolution atmospheric canvas and severe storm nowcasting." />

  <!-- Typography: Plus Jakarta Sans & Inter -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />

  <!-- Leaflet CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

  <style>
    /* ==========================================================================
       1. ATMOSPHERIC CANVAS DESIGN SYSTEM (WARM GRAPHITE & EDITORIAL CHROME)
       ========================================================================== */
    :root {
      /* Warm Graphite Palette */
      --bg-dark-void: #0a0d14;
      --bg-surface: rgba(18, 22, 31, 0.88);
      --bg-surface-solid: #12161f;
      --bg-surface-elevated: #1a202c;
      --bg-surface-hover: #222a3a;

      /* Subtle Hairline Borders */
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-medium: rgba(255, 255, 255, 0.16);
      --border-active: #d97706;

      /* Typography */
      --text-pure: #ffffff;
      --text-warm-white: #f3f4f6;
      --text-primary: #e5e7eb;
      --text-secondary: #9ca3af;
      --text-muted: #6b7280;

      /* Meteorological Spectrum */
      --radar-c20: #0284c7;
      --radar-c35: #10b981;
      --radar-c45: #eab308;
      --radar-c55: #f97316;
      --radar-c65: #dc2626;

      --amber-accent: #d97706;
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
      background: var(--bg-dark-void);
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
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #2b3345; border-radius: 2px; }

    /* ==========================================================================
       2. FULL-SCREEN ATMOSPHERIC ENVIRONMENT (MAP OWNS THE ENTIRE SCREEN)
       ========================================================================== */
    .atmospheric-canvas-root {
      position: absolute;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: 1;
      background: #0e1117;
    }

    #fullScreenVajraMap {
      width: 100%;
      height: 100%;
      background: #0e1117;
    }

    /* AirNet-Grade Cartographic OSM Filter */
    .leaflet-tile-pane {
      filter: brightness(0.62) invert(1) contrast(1.18) hue-rotate(200deg) saturate(0.35);
      transition: filter 0.4s ease;
    }
    .focus-mode-active .leaflet-tile-pane {
      filter: brightness(0.48) invert(1) contrast(1.12) hue-rotate(200deg) saturate(0.25);
    }

    /* ==========================================================================
       3. TOP SITUATION BAR (THIN FLOATING ATMOSPHERIC STATUS LINE)
       ========================================================================== */
    .floating-situation-bar {
      position: absolute;
      top: 18px;
      left: 24px;
      z-index: 1000;
      display: flex;
      align-items: center;
      gap: 16px;
      background: rgba(16, 20, 28, 0.88);
      backdrop-filter: blur(14px);
      border: 1px solid var(--border-medium);
      border-radius: 8px;
      padding: 7px 16px;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.65);
      transition: opacity 0.3s ease, transform 0.3s ease;
    }

    .brand-cluster {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .brand-glyph {
      width: 24px;
      height: 24px;
      border-radius: 5px;
      background: #222938;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .brand-glyph svg {
      width: 15px;
      height: 15px;
      stroke: var(--text-warm-white);
      fill: none;
      stroke-width: 2;
    }

    .brand-title-text {
      font-family: var(--font-display);
      font-size: 15px;
      font-weight: 800;
      letter-spacing: 0.5px;
      color: var(--text-pure);
    }

    .situation-divider {
      width: 1px;
      height: 16px;
      background: var(--border-subtle);
    }

    .atmospheric-telemetry-strip {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 12px;
      color: var(--text-secondary);
    }

    .telemetry-tag-item {
      display: flex;
      align-items: center;
      gap: 5px;
      font-weight: 500;
    }
    .telemetry-tag-item strong {
      color: var(--text-pure);
      font-weight: 700;
    }

    .live-indicator-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 6px #10b981;
    }

    .horizon-badge {
      background: #232a39;
      border: 1px solid var(--border-subtle);
      border-radius: 4px;
      padding: 2px 7px;
      font-size: 11px;
      font-weight: 700;
      color: #f3f4f6;
    }

    /* Mode Segmented Controls */
    .mode-switch-segmented {
      display: flex;
      background: #0f121a;
      border-radius: 5px;
      padding: 2px;
      border: 1px solid var(--border-subtle);
    }

    .mode-tab-button {
      background: none;
      border: none;
      color: var(--text-muted);
      font-family: var(--font-display);
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 3px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .mode-tab-button:hover { color: var(--text-warm-white); }
    .mode-tab-button.active {
      background: #2a3242;
      color: var(--text-pure);
    }

    /* Field View Button */
    .btn-field-view {
      background: none;
      border: 1px solid var(--border-subtle);
      border-radius: 5px;
      padding: 4px 10px;
      font-family: var(--font-display);
      font-size: 11px;
      font-weight: 700;
      color: var(--text-secondary);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
      transition: all 0.15s ease;
    }
    .btn-field-view:hover {
      background: #222938;
      color: var(--text-warm-white);
    }
    .btn-field-view.active {
      background: #2b3345;
      color: #ffffff;
      border-color: rgba(255, 255, 255, 0.3);
    }

    /* ==========================================================================
       4. CONTEXTUAL TOOL DOCK (SLIM VERTICAL INSTRUMENT DOCK NEAR LEFT EDGE)
       ========================================================================== */
    .vertical-instrument-dock {
      position: absolute;
      top: 96px;
      left: 24px;
      z-index: 1000;
      display: flex;
      flex-direction: column;
      gap: 8px;
      transition: opacity 0.3s ease, transform 0.3s ease;
    }

    .dock-pill-bar {
      display: flex;
      flex-direction: column;
      gap: 6px;
      background: rgba(16, 20, 28, 0.88);
      backdrop-filter: blur(14px);
      border: 1px solid var(--border-medium);
      border-radius: 8px;
      padding: 6px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
    }

    .dock-tool-btn {
      width: 38px;
      height: 38px;
      border-radius: 6px;
      background: none;
      border: 1px solid transparent;
      color: var(--text-secondary);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.15s ease;
      position: relative;
    }
    .dock-tool-btn:hover {
      background: #222938;
      color: var(--text-warm-white);
    }
    .dock-tool-btn.active {
      background: #2b3345;
      border-color: rgba(255, 255, 255, 0.25);
      color: var(--text-pure);
    }
    .dock-tool-btn svg {
      width: 18px;
      height: 18px;
      stroke: currentColor;
      fill: none;
      stroke-width: 1.8;
    }

    /* Contextual Popout Surface for Tools (Layers, Storm Selector) */
    .dock-popout-surface {
      position: absolute;
      left: 56px;
      top: 0;
      width: 240px;
      background: rgba(18, 22, 31, 0.94);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-medium);
      border-radius: 8px;
      padding: 12px;
      display: none;
      flex-direction: column;
      gap: 8px;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.75);
    }
    .dock-popout-surface.open {
      display: flex;
    }

    .popout-header {
      font-family: var(--font-display);
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
      border-bottom: 1px solid var(--border-subtle);
      padding-bottom: 6px;
    }

    .popout-item-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 6px 8px;
      border-radius: 4px;
      cursor: pointer;
      font-size: 12px;
      color: var(--text-primary);
      transition: background 0.15s ease;
    }
    .popout-item-row:hover {
      background: #222938;
    }
    .popout-item-row.active {
      color: var(--text-pure);
      font-weight: 600;
      background: rgba(255, 255, 255, 0.05);
    }

    /* ==========================================================================
       5. FLOATING MINI MAP SEARCH (TOP-RIGHT WITH SAFE MARGIN)
       ========================================================================== */
    .floating-mini-search {
      position: absolute;
      top: 18px;
      right: 28px;
      z-index: 1000;
      width: 260px;
      transition: opacity 0.3s ease, transform 0.3s ease;
    }

    .search-box-container {
      position: relative;
      width: 100%;
    }

    .search-field-input {
      width: 100%;
      background: rgba(16, 20, 28, 0.90);
      backdrop-filter: blur(14px);
      border: 1px solid var(--border-medium);
      border-radius: 7px;
      padding: 7px 12px 7px 32px;
      color: var(--text-pure);
      font-family: var(--font-body);
      font-size: 12px;
      outline: none;
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.6);
      transition: all 0.15s ease;
    }
    .search-field-input:focus {
      border-color: rgba(255, 255, 255, 0.35);
      background: rgba(22, 27, 38, 0.98);
    }
    .search-field-input::placeholder {
      color: var(--text-muted);
    }

    .search-input-glyph {
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      width: 14px;
      height: 14px;
      stroke: var(--text-muted);
      fill: none;
      stroke-width: 2;
      pointer-events: none;
    }

    .search-autocomplete-list {
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      margin-top: 5px;
      background: rgba(18, 22, 31, 0.96);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-medium);
      border-radius: 6px;
      max-height: 220px;
      overflow-y: auto;
      display: none;
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.8);
      z-index: 2000;
    }

    .search-result-item {
      padding: 7px 11px;
      font-size: 11.5px;
      color: var(--text-primary);
      border-bottom: 1px solid var(--border-subtle);
      cursor: pointer;
    }
    .search-result-item:hover {
      background: #222938;
      color: #ffffff;
    }

    /* ==========================================================================
       6. CONTEXTUAL STORM INSPECTOR (EMERGENT RIGHT DRAWER / LENS)
       ========================================================================== */
    .contextual-storm-inspector {
      position: absolute;
      top: 18px;
      right: 28px;
      bottom: 24px;
      width: 350px;
      background: rgba(18, 22, 31, 0.92);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-medium);
      border-radius: 10px;
      padding: 20px;
      z-index: 1000;
      display: flex;
      flex-direction: column;
      gap: 16px;
      overflow-y: auto;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.75);
      transform: translateX(390px);
      opacity: 0;
      transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.35s ease;
    }
    .contextual-storm-inspector.open {
      transform: translateX(0);
      opacity: 1;
    }

    .inspector-header-bar {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      border-bottom: 1px solid var(--border-subtle);
      padding-bottom: 12px;
    }

    .inspector-titles {
      display: flex;
      flex-direction: column;
      gap: 3px;
    }

    .storm-identity-title {
      font-family: var(--font-display);
      font-size: 24px;
      font-weight: 800;
      letter-spacing: -0.4px;
      color: var(--text-pure);
    }

    .storm-state-callout {
      font-size: 13px;
      font-weight: 700;
      color: #f87171;
    }

    .btn-close-inspector {
      width: 26px;
      height: 26px;
      border-radius: 4px;
      background: none;
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      transition: all 0.15s ease;
    }
    .btn-close-inspector:hover {
      background: #222938;
      color: var(--text-pure);
    }

    /* 4 Primary Hero Numbers */
    .inspector-metrics-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }

    .inspector-metric-card {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
    }

    .metric-bold-value {
      font-family: var(--font-display);
      font-size: 24px;
      font-weight: 800;
      color: var(--text-pure);
      line-height: 1.1;
    }
    .metric-bold-value.severe-red { color: var(--vermilion-severe); }

    .metric-sub-label {
      font-size: 11px;
      color: var(--text-secondary);
      font-weight: 500;
      margin-top: 3px;
    }

    /* Section: STORM EVOLUTION */
    .inspector-section-block {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .inspector-section-label {
      font-family: var(--font-display);
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
    }

    .evolution-timeline-track {
      display: flex;
      flex-direction: column;
      gap: 7px;
      border-left: 2px solid rgba(255, 255, 255, 0.1);
      margin-left: 6px;
      padding-left: 12px;
    }

    .evolution-node-row {
      display: flex;
      flex-direction: column;
      position: relative;
    }
    .evolution-node-row::before {
      content: "";
      position: absolute;
      left: -17px;
      top: 4px;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #4b5563;
      border: 2px solid #131720;
    }
    .evolution-node-row.done::before { background: #10b981; }
    .evolution-node-row.active-now::before {
      background: var(--vermilion-severe);
      box-shadow: 0 0 6px var(--vermilion-severe);
    }

    .node-timestamp {
      font-size: 10.5px;
      font-weight: 700;
      color: var(--text-muted);
    }
    .node-narrative {
      font-size: 12px;
      font-weight: 500;
      color: var(--text-primary);
    }

    /* Section: WHAT CHANGED */
    .delta-metric-row {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
    }

    .delta-pill-card {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border-subtle);
      border-radius: 5px;
      padding: 8px 10px;
      display: flex;
      flex-direction: column;
    }
    .delta-title { font-size: 10.5px; color: var(--text-secondary); }
    .delta-number {
      font-family: var(--font-display);
      font-size: 15px;
      font-weight: 800;
      color: var(--vermilion-severe);
    }

    /* Section: IMPACT INTERSECTIONS */
    .impact-corridor-stack {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .impact-item-row {
      background: rgba(255, 255, 255, 0.04);
      border-left: 3px solid #d97706;
      border-radius: 0 5px 5px 0;
      padding: 8px 10px;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    .impact-row-header {
      font-size: 12px;
      font-weight: 700;
      color: var(--text-pure);
      display: flex;
      justify-content: space-between;
    }
    .impact-row-body {
      font-size: 11px;
      color: var(--text-secondary);
      line-height: 1.35;
    }

    /* ==========================================================================
       7. MINIMAL FORECAST SCRUBBER (FLOATING MAP INSTRUMENT)
       ========================================================================== */
    .floating-forecast-instrument {
      position: absolute;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 1000;
      background: rgba(16, 20, 28, 0.90);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-medium);
      border-radius: 30px;
      padding: 8px 20px;
      display: flex;
      align-items: center;
      gap: 18px;
      box-shadow: 0 10px 32px rgba(0, 0, 0, 0.7);
      transition: opacity 0.3s ease, transform 0.3s ease;
    }

    .btn-play-evolution {
      background: #2a3242;
      border: 1px solid var(--border-subtle);
      border-radius: 20px;
      padding: 5px 14px;
      color: var(--text-pure);
      font-family: var(--font-display);
      font-size: 12px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .btn-play-evolution:hover {
      background: #353f54;
      border-color: rgba(255, 255, 255, 0.3);
    }

    .timeline-spatial-spine {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .spine-step-button {
      background: none;
      border: none;
      color: var(--text-muted);
      font-family: var(--font-display);
      font-size: 11.5px;
      font-weight: 600;
      cursor: pointer;
      padding: 3px 6px;
      border-radius: 4px;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .spine-step-button:hover { color: var(--text-warm-white); }
    .spine-step-button.active {
      color: var(--text-pure);
      font-weight: 800;
    }
    .spine-step-button .dot-indicator {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #374151;
      transition: all 0.15s ease;
    }
    .spine-step-button.active .dot-indicator {
      background: #fde047;
      box-shadow: 0 0 8px #fde047;
      transform: scale(1.4);
    }

    /* ==========================================================================
       8. FOCUS MODE RETURN PILL
       ========================================================================== */
    .focus-mode-banner {
      position: absolute;
      top: 74px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 1000;
      background: rgba(220, 38, 38, 0.18);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(220, 38, 38, 0.4);
      border-radius: 20px;
      padding: 5px 14px;
      font-family: var(--font-display);
      font-size: 11.5px;
      font-weight: 700;
      color: #fca5a5;
      display: none;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
    }
    .focus-mode-banner.active {
      display: flex;
    }
    .focus-mode-banner:hover {
      background: rgba(220, 38, 38, 0.28);
    }

    /* ==========================================================================
       9. MAP-NATIVE SCIENTIFIC METEOROLOGICAL MARKERS
       ========================================================================== */
    .scientific-cell-glyph {
      width: 38px;
      height: 38px;
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
      transition: transform 0.2s ease;
    }
    .scientific-cell-glyph:hover {
      transform: scale(1.1);
    }

    .scientific-lightning-pulse {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #fde047;
      box-shadow: 0 0 10px #fde047;
      animation: pulse-lightning 1.6s infinite ease-out;
    }
    @keyframes pulse-lightning {
      0% { transform: scale(0.3); opacity: 1; }
      50% { transform: scale(2.2); opacity: 0.6; }
      100% { transform: scale(3.4); opacity: 0; }
    }

    .geotag-city-pill {
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

    /* Spatial What-Changed Delta Tag near Storm on Map */
    .spatial-delta-annotation {
      background: rgba(26, 31, 44, 0.94);
      border: 1px solid #d97706;
      border-radius: 5px;
      padding: 4px 8px;
      font-family: var(--font-display);
      font-size: 10.5px;
      font-weight: 700;
      color: #fef08a;
      box-shadow: 0 4px 16px rgba(0,0,0,0.6);
      white-space: nowrap;
      pointer-events: none;
    }

    /* FIELD VIEW MODE (HIDES ALL CHROME EXCEPT MAP & MINIMAL SCRUBBER) */
    .field-view-active .floating-situation-bar,
    .field-view-active .vertical-instrument-dock,
    .field-view-active .floating-mini-search,
    .field-view-active .contextual-storm-inspector {
      opacity: 0 !important;
      pointer-events: none !important;
      transform: translateY(-20px) !important;
    }
  </style>
</head>
<body>

  <!-- ==========================================================================
       1. THE FULLSCREEN LIVING ATMOSPHERIC CANVAS (EDGE-TO-EDGE)
       ========================================================================== -->
  <div class="atmospheric-canvas-root" id="canvasRoot">
    <div id="fullScreenVajraMap"></div>
  </div>

  <!-- ==========================================================================
       2. FLOATING SITUATION BAR (THIN ATMOSPHERIC STATUS LINE)
       ========================================================================== -->
  <div class="floating-situation-bar" id="situationStatusBar">
    <div class="brand-cluster">
      <div class="brand-glyph">
        <svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8zm0-14a6 6 0 0 0-6 6h6z"/></svg>
      </div>
      <span class="brand-title-text">VAJRA</span>
    </div>

    <div class="situation-divider"></div>

    <div class="atmospheric-telemetry-strip">
      <div class="telemetry-tag-item">
        <span class="live-indicator-dot"></span>
        <span>EASTERN INDIA</span>
      </div>
      <span>&bull;</span>
      <div class="telemetry-tag-item">
        <strong>12</strong> Active
      </div>
      <span>&bull;</span>
      <div class="telemetry-tag-item">
        <strong style="color:#f87171;">4</strong> Intensifying
      </div>
      <span>&bull;</span>
      <div class="telemetry-tag-item">
        <strong style="color:#fde047;">1</strong> High Impact
      </div>
    </div>

    <div class="situation-divider"></div>

    <!-- Segmented Mode Control -->
    <div class="mode-switch-segmented">
      <button class="mode-tab-button" id="btnModeObserved">OBSERVED</button>
      <button class="mode-tab-button active" id="btnModeNowcast">NOWCAST</button>
    </div>

    <!-- Field View Mode Toggle -->
    <button class="btn-field-view" id="btnToggleFieldView" title="Toggle Clean Field View (Presentation Mode)">
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg>
      <span>FIELD VIEW</span>
    </button>
  </div>

  <!-- ==========================================================================
       3. CONTEXTUAL TOOL DOCK (SLIM VERTICAL DOCK NEAR LEFT EDGE)
       ========================================================================== -->
  <div class="vertical-instrument-dock" id="verticalToolDock">
    <div class="dock-pill-bar">
      <!-- Layers Popout Toggle -->
      <button class="dock-tool-btn active" id="btnDockLayers" title="Atmospheric Layers">
        <svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
      </button>

      <!-- Tracked Storms Popout Toggle -->
      <button class="dock-tool-btn" id="btnDockStorms" title="Tracked Storm Cells">
        <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M22 12h-4M6 12H2M12 6V2M12 22v-4"/></svg>
      </button>

      <!-- Impact Lens Toggle -->
      <button class="dock-tool-btn" id="btnDockImpact" title="Impact Lens (Infrastructure Intersections)">
        <svg viewBox="0 0 24 24"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
      </button>

      <!-- Reset / Regional View -->
      <button class="dock-tool-btn" id="btnDockResetView" title="Reset to Regional Overview">
        <svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8M3 3v5h5"/></svg>
      </button>
    </div>

    <!-- Layers Popout Surface -->
    <div class="dock-popout-surface" id="layersPopoutSurface">
      <div class="popout-header">
        <span>ATMOSPHERIC LAYERS</span>
        <span style="cursor:pointer;" id="btnCloseLayersPopout">&times;</span>
      </div>
      <div class="popout-item-row active" id="popLayerRadar">
        <span>Radar Reflectivity</span>
        <span style="color:#10b981; font-size:10px;">LIVE</span>
      </div>
      <div class="popout-item-row active" id="popLayerSat">
        <span>Satellite Cloud Top</span>
        <span style="color:#9ca3af; font-size:10px;">8m ago</span>
      </div>
      <div class="popout-item-row active" id="popLayerLtg">
        <span>Lightning Discharges</span>
        <span style="color:#fde047; font-size:10px;">REALTIME</span>
      </div>
      <div class="popout-item-row active" id="popLayerTracks">
        <span>Storm Trajectories</span>
        <span style="color:#a855f7; font-size:10px;">FORECAST</span>
      </div>
    </div>

    <!-- Storms Popout Surface -->
    <div class="dock-popout-surface" id="stormsPopoutSurface">
      <div class="popout-header">
        <span>ACTIVE STORMS</span>
        <span style="cursor:pointer;" id="btnCloseStormsPopout">&times;</span>
      </div>
      <div class="popout-item-row active" onclick="triggerStormFocus('024')">
        <span>Cell 024 (Midnapore)</span>
        <span style="color:#dc2626; font-weight:700;">68 dBZ</span>
      </div>
      <div class="popout-item-row" onclick="triggerStormFocus('018')">
        <span>Cell 018 (Burdwan)</span>
        <span style="color:#f59e0b; font-weight:700;">52 dBZ</span>
      </div>
      <div class="popout-item-row" onclick="triggerStormFocus('031')">
        <span>Cell 031 (Balasore)</span>
        <span style="color:#dc2626; font-weight:700;">59 dBZ</span>
      </div>
    </div>
  </div>

  <!-- ==========================================================================
       4. FLOATING MINI MAP SEARCH (TOP-RIGHT WITH SAFE MARGIN)
       ========================================================================== -->
  <div class="floating-mini-search" id="miniMapSearchBox">
    <div class="search-box-container">
      <svg class="search-input-glyph" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
      <input type="text" class="search-field-input" id="osmMiniSearchInput" placeholder="Search city, district or location..." autocomplete="off" />
      <div class="search-autocomplete-list" id="searchAutocompleteList"></div>
    </div>
  </div>

  <!-- ==========================================================================
       5. FOCUS MODE RETURN PILL
       ========================================================================== -->
  <div class="focus-mode-banner active" id="focusModeBanner" onclick="exitFocusToRegional()">
    <span>🔍 FOCUS: CELL 024 &bull; CLICK TO RETURN TO REGIONAL OVERVIEW</span>
  </div>

  <!-- ==========================================================================
       6. CONTEXTUAL STORM INSPECTOR (EMERGENT RIGHT DRAWER / LENS)
       ========================================================================== -->
  <div class="contextual-storm-inspector open" id="stormInspectorDrawer">
    <div class="inspector-header-bar">
      <div class="inspector-titles">
        <span class="storm-identity-title" id="inspectorStormTitle">STORM CELL 024</span>
        <span class="storm-state-callout" id="inspectorStateCallout">RAPIDLY INTENSIFYING</span>
      </div>
      <button class="btn-close-inspector" id="btnCloseInspector" title="Collapse Inspector">&times;</button>
    </div>

    <!-- 4 Primary Numbers -->
    <div class="inspector-metrics-grid">
      <div class="inspector-metric-card">
        <span class="metric-bold-value severe-red" id="inspDbz">68 dBZ</span>
        <span class="metric-sub-label">Current intensity</span>
      </div>
      <div class="inspector-metric-card">
        <span class="metric-bold-value" id="inspSpeed">34 km/h</span>
        <span class="metric-sub-label" id="inspDir">SOUTHEAST</span>
      </div>
      <div class="inspector-metric-card">
        <span class="metric-bold-value" id="inspEta">18–27 min</span>
        <span class="metric-sub-label">Arrival window</span>
      </div>
      <div class="inspector-metric-card">
        <span class="metric-bold-value" id="inspConfidence">87%</span>
        <span class="metric-sub-label">Forecast confidence</span>
      </div>
    </div>

    <!-- EVOLUTION Narrative Timeline -->
    <div class="inspector-section-block">
      <div class="inspector-section-label">
        <span>STORM EVOLUTION</span>
        <span style="color:#d97706;">5 PHASES</span>
      </div>
      <div class="evolution-timeline-track" id="inspectorEvolutionTrack">
        <div class="evolution-node-row done">
          <span class="node-timestamp">14:10 &bull; FORMED</span>
          <span class="node-narrative">Initiated in Midnapore sector (38 dBZ)</span>
        </div>
        <div class="evolution-node-row done">
          <span class="node-timestamp">14:18 &bull; DEVELOPING</span>
          <span class="node-narrative">Reflectivity surge (+10 dBZ in 8 min)</span>
        </div>
        <div class="evolution-node-row done">
          <span class="node-timestamp">14:26 &bull; LIGHTNING ACCELERATION</span>
          <span class="node-narrative">Discharge rate spiked to 38 strokes/min</span>
        </div>
        <div class="evolution-node-row active-now">
          <span class="node-timestamp">14:34 &bull; INTENSIFYING (NOW)</span>
          <span class="node-narrative">Severe hail core with overshooting convective top</span>
        </div>
        <div class="evolution-node-row">
          <span class="node-timestamp">14:50 &bull; PROJECTED PEAK</span>
          <span class="node-narrative">Direct crossing of Kolkata-Howrah urban corridor</span>
        </div>
      </div>
    </div>

    <!-- WHAT CHANGED -->
    <div class="inspector-section-block">
      <div class="inspector-section-label">
        <span>WHAT CHANGED &bull; LAST 15 MIN</span>
        <span style="color:#dc2626;">↗ ESCALATING</span>
      </div>
      <div class="delta-metric-row">
        <div class="delta-pill-card">
          <span class="delta-title">Radar growth</span>
          <span class="delta-number">+14 dBZ</span>
        </div>
        <div class="delta-pill-card">
          <span class="delta-title">Lightning activity</span>
          <span class="delta-number">+27%</span>
        </div>
        <div class="delta-pill-card">
          <span class="delta-title">Cloud cooling</span>
          <span class="delta-number" style="color:#38bdf8;">&darr; -6.2&deg;C</span>
        </div>
        <div class="delta-pill-card">
          <span class="delta-title">Storm area</span>
          <span class="delta-number">+18%</span>
        </div>
      </div>
    </div>

    <!-- POTENTIAL IMPACT -->
    <div class="inspector-section-block">
      <div class="inspector-section-label">
        <span>IMPACT INTERSECTIONS</span>
        <span style="color:#d97706;">CORRIDOR</span>
      </div>
      <div class="impact-corridor-stack">
        <div class="impact-item-row">
          <div class="impact-row-header">
            <span>✈ VECC Kolkata Airport</span>
            <span style="color:#dc2626;">ETA 22m</span>
          </div>
          <span class="impact-row-body">Microburst risk across runway 19L/01R. Holding advised.</span>
        </div>
        <div class="impact-item-row">
          <div class="impact-row-header">
            <span>🛣 Highways NH-16 &amp; NH-19</span>
            <span style="color:#d97706;">ETA 14m</span>
          </div>
          <span class="impact-row-body">Direct squall crossing with crosswinds &gt; 75 km/h.</span>
        </div>
        <div class="impact-item-row">
          <div class="impact-row-header">
            <span>⚡ 765kV Regional Substation</span>
            <span style="color:#f97316;">High Risk</span>
          </div>
          <span class="impact-row-body">High-density CG lightning strike cluster in sector.</span>
        </div>
      </div>
    </div>
  </div>

  <!-- ==========================================================================
       7. MINIMAL FORECAST SCRUBBER (FLOATING MAP INSTRUMENT)
       ========================================================================== -->
  <div class="floating-forecast-instrument" id="floatingForecastInstrument">
    <button class="btn-play-evolution" id="btnPlayEvolution">
      <span id="playIconSpan">▶</span>
      <span id="playTextSpan">PLAY EVOLUTION</span>
    </button>

    <div class="timeline-spatial-spine">
      <button class="spine-step-button" data-idx="0">
        <span class="dot-indicator"></span>
        <span>NOW</span>
      </button>
      <button class="spine-step-button" data-idx="1">
        <span class="dot-indicator"></span>
        <span>+15m</span>
      </button>
      <button class="spine-step-button active" data-idx="2">
        <span class="dot-indicator"></span>
        <span>+30m</span>
      </button>
      <button class="spine-step-button" data-idx="3">
        <span class="dot-indicator"></span>
        <span>+45m</span>
      </button>
      <button class="spine-step-button" data-idx="4">
        <span class="dot-indicator"></span>
        <span>+60m</span>
      </button>
      <button class="spine-step-button" data-idx="5">
        <span class="dot-indicator"></span>
        <span>+90m</span>
      </button>
      <button class="spine-step-button" data-idx="6">
        <span class="dot-indicator"></span>
        <span>+120m</span>
      </button>
    </div>
  </div>

  <!-- ==========================================================================
       8. JAVASCRIPT: THE SPATIAL REVOLUTION ENGINE
       ========================================================================== -->
  <script>
    /* ==========================================================================
       DATA CATALOG
       ========================================================================== */
    const STORM_DB = {
      '024': {
        id: 'STORM CELL 024',
        callout: 'RAPIDLY INTENSIFYING',
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
          { time: '14:10 \u2022 FORMED', narrative: 'Initiated in Midnapore sector (38 dBZ)', status: 'done' },
          { time: '14:18 \u2022 DEVELOPING', narrative: 'Reflectivity surge (+10 dBZ in 8 min)', status: 'done' },
          { time: '14:26 \u2022 LIGHTNING ACCELERATION', narrative: 'Discharge rate spiked to 38 strokes/min', status: 'done' },
          { time: '14:34 \u2022 INTENSIFYING (NOW)', narrative: 'Severe hail core with overshooting convective top', status: 'active-now' },
          { time: '14:50 \u2022 PROJECTED PEAK', narrative: 'Direct crossing of Kolkata-Howrah urban corridor', status: 'pending' }
        ]
      },
      '018': {
        id: 'STORM CELL 018',
        callout: 'FORWARD ADVECTION',
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
          { time: '13:55 \u2022 FORMED', narrative: 'Burdwan convective initiation', status: 'done' },
          { time: '14:15 \u2022 DEVELOPING', narrative: 'Cluster consolidating eastwards', status: 'done' },
          { time: '14:34 \u2022 ADVECTION (NOW)', narrative: 'Steady moderate precipitation band', status: 'active-now' },
          { time: '15:10 \u2022 PASSAGE', narrative: 'Passing Ranaghat railway hub', status: 'pending' }
        ]
      },
      '031': {
        id: 'STORM CELL 031',
        callout: 'COASTAL SQUALL SEGMENT',
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
          { time: '14:00 \u2022 FORMED', narrative: 'Balasore coastal squall initiation', status: 'done' },
          { time: '14:20 \u2022 BOWING', narrative: 'Bow echo segment developing with gust front', status: 'done' },
          { time: '14:34 \u2022 SEVERE (NOW)', narrative: 'Approaching Digha coastal defense line', status: 'active-now' },
          { time: '15:00 \u2022 INDUSTRIAL PASSAGE', narrative: 'Haldia port & petrochem industrial zone', status: 'pending' }
        ]
      }
    };

    let activeStormKey = '024';
    let currentStep = 2; // +30m
    let currentMode = 'nowcast'; // 'observed' or 'nowcast'
    let isFieldView = false;
    let isImpactLens = false;
    let isPlaying = false;
    let playTimer = null;

    let map = null;
    let layerRadar = null;
    let layerSat = null;
    let layerLtg = null;
    let layerTracks = null;
    let layerImpact = null;
    let layerDeltas = null;

    /* ==========================================================================
       INITIALIZATION
       ========================================================================== */
    window.addEventListener('DOMContentLoaded', () => {
      initEdgeToEdgeMap();
      setupSpatialInteractions();
      renderAtmosphericEnvironment();
    });

    /* ==========================================================================
       MAP INITIALIZATION (EDGE TO EDGE FULLSCREEN)
       ========================================================================== */
    function initEdgeToEdgeMap() {
      map = L.map('fullScreenVajraMap', {
        zoomControl: false,
        attributionControl: false,
        preferCanvas: true
      }).setView([22.60, 88.20], 9);

      L.control.zoom({ position: 'bottomleft' }).addTo(map);

      // True OpenStreetMap Cartography
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        opacity: 0.95
      }).addTo(map);

      // Map Layers
      layerRadar = L.layerGroup().addTo(map);
      layerSat = L.layerGroup().addTo(map);
      layerLtg = L.layerGroup().addTo(map);
      layerTracks = L.layerGroup().addTo(map);
      layerImpact = L.layerGroup().addTo(map);
      layerDeltas = L.layerGroup().addTo(map);

      // Subtle City Geotags
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
          className: 'city-badge-wrap',
          html: `<div class="geotag-city-pill">${c.name}</div>`,
          iconSize: [60, 18],
          iconAnchor: [30, 9]
        });
        L.marker([c.lat, c.lon], { icon: badge, interactive: false }).addTo(map);
      });
    }

    /* ==========================================================================
       SCIENTIFIC ATMOSPHERIC RENDERING
       ========================================================================== */
    function renderAtmosphericEnvironment() {
      layerRadar.clearLayers();
      layerLtg.clearLayers();
      layerTracks.clearLayers();
      layerImpact.clearLayers();
      layerDeltas.clearLayers();

      const storm = STORM_DB[activeStormKey];
      const track = storm.track;

      // 1. FORECAST UNCERTAINTY FIELD (Soft, feathered probabilistic envelope)
      if (currentMode === 'nowcast') {
        const p0 = track[0];
        const pTarget = track[currentStep] || track[track.length - 1];
        const spread = 0.08 + (currentStep * 0.05);

        const fieldCoords = [
          [p0[0], p0[1]],
          [pTarget[0] + spread * 0.75, pTarget[1] - spread],
          [pTarget[0] + spread * 1.15, pTarget[1] + spread],
          [pTarget[0] - spread * 0.55, pTarget[1] + spread * 0.85],
          [p0[0], p0[1]]
        ];

        L.polygon(fieldCoords, {
          color: '#a855f7',
          fillColor: '#a855f7',
          fillOpacity: 0.12,
          weight: 1.5,
          dashArray: '4, 6'
        }).addTo(layerTracks);
      }

      // 2. DIRECTIONAL TRAJECTORY
      L.polyline(track, {
        color: '#f59e0b',
        weight: 2.5,
        opacity: 0.85,
        dashArray: '5, 5'
      }).addTo(layerTracks);

      // 3. CURRENT STORM MULTI-CONTOUR REFLECTIVITY
      const t0 = track[0];

      // Outer Footprint (35 dBZ)
      L.circle(t0, {
        radius: 22000,
        color: '#10b981',
        fillColor: '#10b981',
        fillOpacity: 0.28,
        weight: 1
      }).addTo(layerRadar);

      // Elevated Band (50 dBZ)
      L.circle(t0, {
        radius: 13000,
        color: '#f97316',
        fillColor: '#f97316',
        fillOpacity: 0.5,
        weight: 1.5
      }).addTo(layerRadar);

      // Severe Hail Core (65+ dBZ)
      L.circle(t0, {
        radius: 6500,
        color: '#dc2626',
        fillColor: '#dc2626',
        fillOpacity: 0.8,
        weight: 2
      }).addTo(layerRadar);

      // 4. STORM SHADOWS (Progressively Translucent Future Footprints)
      if (currentMode === 'nowcast') {
        const stepNames = ['NOW', '+15m', '+30m', '+45m', '+60m', '+90m', '+120m'];

        for (let i = 1; i <= currentStep; i++) {
          const pt = track[i];
          if (!pt) continue;

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

          L.circleMarker(pt, {
            radius: 5,
            color: '#f59e0b',
            fillColor: '#11141c',
            fillOpacity: 1,
            weight: 2
          }).bindTooltip(`${stepNames[i]} position (${storm.id})`, { permanent: false }).addTo(layerTracks);
        }
      }

      // 5. ACTIVE STORM CELL CENTROID RING
      const activeCentroid = (currentMode === 'nowcast' && currentStep > 0) ? track[currentStep] : t0;
      const coreIcon = L.divIcon({
        className: 'storm-glyph-wrap',
        html: `<div class="scientific-cell-glyph" title="${storm.id}">${parseInt(storm.dbz)}</div>`,
        iconSize: [38, 38],
        iconAnchor: [19, 19]
      });
      const marker = L.marker(activeCentroid, { icon: coreIcon }).addTo(layerTracks);
      marker.on('click', () => {
        openStormInspector(activeStormKey);
      });

      // 6. SPATIAL WHAT-CHANGED DELTA TAG (MAP ANNOTATION)
      const deltaTag = L.divIcon({
        className: 'delta-annotation-wrap',
        html: `<div class="spatial-delta-annotation">+14 dBZ &bull; +27% LTG &bull; ESCALATING</div>`,
        iconSize: [180, 24],
        iconAnchor: [-10, 30]
      });
      L.marker(activeCentroid, { icon: deltaTag, interactive: false }).addTo(layerDeltas);

      // 7. SCIENTIFIC LIGHTNING DISCHARGES
      storm.lightnings.forEach(lt => {
        const ltIcon = L.divIcon({
          className: 'lt-pulse-wrap',
          html: '<div class="scientific-lightning-pulse"></div>',
          iconSize: [10, 10],
          iconAnchor: [5, 5]
        });
        L.marker(lt, { icon: ltIcon }).addTo(layerLtg);
      });

      // 8. IMPACT LENS INTERSECTIONS
      if (isImpactLens) {
        const assets = [
          { name: "VECC Kolkata Airport", pt: [22.654, 88.446], desc: "Runway approach crossing in 22 min" },
          { name: "NH-16 & NH-19 Highway Hub", pt: [22.48, 87.95], desc: "Direct squall crossing (75 km/h gusts)" },
          { name: "765kV Regional Substation", pt: [22.42, 87.35], desc: "High CG lightning strike cluster" }
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
       STORM FOCUS & INSPECTOR LOGIC
       ========================================================================== */
    function triggerStormFocus(stormKey) {
      activeStormKey = stormKey;
      const storm = STORM_DB[stormKey];

      // Close popouts
      closeAllPopouts();

      // Open Inspector Drawer
      openStormInspector(stormKey);

      // Map Smooth Zoom Focus
      document.body.classList.add('focus-mode-active');
      document.getElementById('focusModeBanner').classList.add('active');
      document.getElementById('focusModeBanner').innerHTML = `<span>🔍 FOCUS: CELL ${stormKey} &bull; CLICK TO RETURN TO REGIONAL OVERVIEW</span>`;

      map.flyTo(storm.center, 9.5, { duration: 1.2 });

      renderAtmosphericEnvironment();
    }

    function openStormInspector(stormKey) {
      activeStormKey = stormKey;
      const storm = STORM_DB[stormKey];

      document.getElementById('inspectorStormTitle').textContent = storm.id;
      document.getElementById('inspectorStateCallout').textContent = storm.callout;
      document.getElementById('inspDbz').textContent = storm.dbz;
      document.getElementById('inspSpeed').textContent = storm.speed;
      document.getElementById('inspDir').textContent = storm.direction;
      document.getElementById('inspEta').textContent = storm.arrival;
      document.getElementById('inspConfidence').textContent = storm.confidence;

      // Update Evolution Track
      const trackContainer = document.getElementById('inspectorEvolutionTrack');
      trackContainer.innerHTML = '';
      storm.story.forEach(s => {
        const row = document.createElement('div');
        row.className = `evolution-node-row ${s.status}`;
        row.innerHTML = `
          <span class="node-timestamp">${s.time}</span>
          <span class="node-narrative">${s.narrative}</span>
        `;
        trackContainer.appendChild(row);
      });

      document.getElementById('stormInspectorDrawer').classList.add('open');
    }

    function exitFocusToRegional() {
      document.body.classList.remove('focus-mode-active');
      document.getElementById('focusModeBanner').classList.remove('active');
      document.getElementById('stormInspectorDrawer').classList.remove('open');
      map.flyTo([22.65, 88.25], 8, { duration: 1.0 });
    }

    /* ==========================================================================
       TIMELINE STEPPING
       ========================================================================== */
    function setSpineStep(stepIdx) {
      currentStep = stepIdx;

      document.querySelectorAll('.spine-step-button').forEach((btn, i) => {
        btn.classList.toggle('active', i === stepIdx);
      });

      renderAtmosphericEnvironment();
    }

    /* ==========================================================================
       SEARCH & POPOUTS
       ========================================================================== */
    function closeAllPopouts() {
      document.getElementById('layersPopoutSurface').classList.remove('open');
      document.getElementById('stormsPopoutSurface').classList.remove('open');
      document.getElementById('btnDockLayers').classList.remove('active');
      document.getElementById('btnDockStorms').classList.remove('active');
    }

    function setupSpatialInteractions() {
      // Inspector Close
      document.getElementById('btnCloseInspector').addEventListener('click', () => {
        document.getElementById('stormInspectorDrawer').classList.remove('open');
      });

      // Dock Buttons
      document.getElementById('btnDockLayers').addEventListener('click', () => {
        const surface = document.getElementById('layersPopoutSurface');
        const isOpen = surface.classList.contains('open');
        closeAllPopouts();
        if (!isOpen) {
          surface.classList.add('open');
          document.getElementById('btnDockLayers').classList.add('active');
        }
      });

      document.getElementById('btnDockStorms').addEventListener('click', () => {
        const surface = document.getElementById('stormsPopoutSurface');
        const isOpen = surface.classList.contains('open');
        closeAllPopouts();
        if (!isOpen) {
          surface.classList.add('open');
          document.getElementById('btnDockStorms').classList.add('active');
        }
      });

      document.getElementById('btnDockImpact').addEventListener('click', () => {
        isImpactLens = !isImpactLens;
        document.getElementById('btnDockImpact').classList.toggle('active', isImpactLens);
        renderAtmosphericEnvironment();
      });

      document.getElementById('btnDockResetView').addEventListener('click', () => {
        exitFocusToRegional();
      });

      document.getElementById('btnCloseLayersPopout').addEventListener('click', closeAllPopouts);
      document.getElementById('btnCloseStormsPopout').addEventListener('click', closeAllPopouts);

      // Field View Toggle (Clean Presentation Mode)
      document.getElementById('btnToggleFieldView').addEventListener('click', () => {
        isFieldView = !isFieldView;
        document.body.classList.toggle('field-view-active', isFieldView);
        document.getElementById('btnToggleFieldView').classList.toggle('active', isFieldView);
      });

      // Observed / Nowcast Segmented Buttons
      document.getElementById('btnModeObserved').addEventListener('click', () => {
        currentMode = 'observed';
        document.getElementById('btnModeObserved').classList.add('active');
        document.getElementById('btnModeNowcast').classList.remove('active');
        renderAtmosphericEnvironment();
      });

      document.getElementById('btnModeNowcast').addEventListener('click', () => {
        currentMode = 'nowcast';
        document.getElementById('btnModeNowcast').classList.add('active');
        document.getElementById('btnModeObserved').classList.remove('active');
        renderAtmosphericEnvironment();
      });

      // Timeline Buttons
      document.querySelectorAll('.spine-step-button').forEach(btn => {
        btn.addEventListener('click', () => {
          setSpineStep(parseInt(btn.dataset.idx));
        });
      });

      // Play Evolution
      const playBtn = document.getElementById('btnPlayEvolution');
      const playIcon = document.getElementById('playIconSpan');
      const playText = document.getElementById('playTextSpan');

      playBtn.addEventListener('click', () => {
        isPlaying = !isPlaying;
        if (isPlaying) {
          playIcon.textContent = '⏸';
          playText.textContent = 'PAUSE';
          playTimer = setInterval(() => {
            let next = (currentStep + 1) % 7;
            setSpineStep(next);
          }, 1600);
        } else {
          playIcon.textContent = '▶';
          playText.textContent = 'PLAY EVOLUTION';
          clearInterval(playTimer);
        }
      });

      // Mini Map Search Integration
      const searchInput = document.getElementById('osmMiniSearchInput');
      const searchDropdown = document.getElementById('searchAutocompleteList');

      let debounce = null;
      searchInput.addEventListener('input', () => {
        clearTimeout(debounce);
        const q = searchInput.value.trim();
        if (q.length < 2) {
          searchDropdown.style.display = 'none';
          return;
        }

        debounce = setTimeout(async () => {
          try {
            let data = null;
            try {
              const resp = await fetch(`/osm/search?q=${encodeURIComponent(q)}`);
              if (resp.ok) data = await resp.json();
            } catch(e) {}

            if (!data || !data.results || data.results.length === 0) {
              const direct = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(q)}&format=json&limit=5&countrycodes=in`);
              if (direct.ok) {
                const raw = await direct.json();
                data = { results: raw.map(r => ({ display_name: r.display_name, lat: parseFloat(r.lat), lon: parseFloat(r.lon) })) };
              }
            }

            if (data && data.results && data.results.length > 0) {
              searchDropdown.innerHTML = '';
              data.results.forEach(res => {
                const row = document.createElement('div');
                row.className = 'search-result-item';
                row.textContent = res.display_name;
                row.addEventListener('click', () => {
                  searchDropdown.style.display = 'none';
                  searchInput.value = res.display_name.split(',')[0];
                  map.flyTo([res.lat, res.lon], 11, { duration: 1.2 });
                });
                searchDropdown.appendChild(row);
              });
              searchDropdown.style.display = 'block';
            } else {
              searchDropdown.style.display = 'none';
            }
          } catch(err) {
            searchDropdown.style.display = 'none';
          }
        }, 300);
      });

      document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
          searchDropdown.style.display = 'none';
        }
      });

      // Popout Layer Items
      const bindPopLayer = (id, layer) => {
        const el = document.getElementById(id);
        el.addEventListener('click', () => {
          el.classList.toggle('active');
          if (el.classList.contains('active')) map.addLayer(layer);
          else map.removeLayer(layer);
        });
      };
      bindPopLayer('popLayerRadar', layerRadar);
      bindPopLayer('popLayerSat', layerSat);
      bindPopLayer('popLayerLtg', layerLtg);
      bindPopLayer('popLayerTracks', layerTracks);
    }
  </script>
</body>
</html>
"""

with open("dashboard/index.html", "w", encoding="utf-8") as f:
    f.write(code)

print(f"Generated Revolutionary VAJRA Spatial Environment: {len(code)} bytes")
