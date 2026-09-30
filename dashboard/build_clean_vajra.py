# -*- coding: utf-8 -*-
"""
VAJRA Atmospheric Intelligence Platform - Ground-up Redesign
Design Philosophy:
- Atmosphere First. Data Second. UI Third.
- Google Earth / Mapbox quality + Apple-level polish + Aviation-grade information design
- Map is the hero (~70% of viewport)
- Large, comfortable typography (16-22px body, 28-36px hero metrics)
- Deep blue-charcoal / midnight navy palette with translucent frosted glass panels
- Fully functioning Leaflet map with multi-source basemaps and vector fallback
- Signature Storm Shadow (progressively translucent future footprints), uncertainty corridor, and clean trajectory
- Contextual intelligence panel (Storm Cell 024, Rapidly Intensifying, 4 key metrics, Why is it intensifying?, Potential impact)
- Bottom forecast timeline with Play/Pause and Observed/Nowcast toggle
"""

html_code = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>VAJRA — Atmospheric Intelligence Platform</title>
  <meta name="description" content="VAJRA: Very-short-term Atmospheric Risk & Joint Analysis. AIML-based Nowcasting of Thunderstorm and Lightning over India." />

  <!-- Google Fonts: Plus Jakarta Sans & Inter -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />

  <!-- Leaflet CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

  <style>
    /* ==========================================================================
       PREMIUM ATMOSPHERIC DESIGN SYSTEM
       ========================================================================== */
    :root {
      /* Backgrounds: Deep Blue-Charcoal / Midnight Navy */
      --bg-canvas: #090e17;
      --bg-panel: rgba(14, 21, 37, 0.88);
      --bg-panel-solid: #0e1525;
      --bg-panel-elevated: #162035;
      --bg-panel-hover: #1c2842;
      --bg-pill: rgba(255, 255, 255, 0.06);
      --bg-pill-hover: rgba(255, 255, 255, 0.12);

      /* Borders: Subtle, Elegant */
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-medium: rgba(255, 255, 255, 0.15);
      --border-focus: #38bdf8;

      /* Typography Colors */
      --text-white: #ffffff;
      --text-primary: #f1f5f9;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;

      /* Meaningful Atmospheric Accents */
      --cyan-obs: #06b6d4;
      --blue-nowcast: #3b82f6;
      --amber-dev: #f59e0b;
      --orange-elev: #f97316;
      --red-severe: #ef4444;
      --violet-uncert: #a855f7;
      --green-live: #10b981;

      /* Fonts */
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
      font-size: 14px;
      line-height: 1.5;
      height: 100vh;
      width: 100vw;
      overflow: hidden;
      user-select: none;
    }

    /* ==========================================================================
       HEADER: ELEGANT, MINIMAL PRODUCT HEADER
       ========================================================================== */
    .product-header {
      height: 64px;
      background: var(--bg-panel-solid);
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
      z-index: 1000;
      position: relative;
    }

    .header-left {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .brand-logo-mark {
      width: 36px;
      height: 36px;
      border-radius: 8px;
      background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35);
    }
    .brand-logo-mark svg {
      width: 22px;
      height: 22px;
      fill: #ffffff;
    }

    .brand-title-wrap {
      display: flex;
      flex-direction: column;
    }

    .brand-title {
      font-family: var(--font-display);
      font-size: 20px;
      font-weight: 800;
      letter-spacing: -0.5px;
      color: var(--text-white);
      line-height: 1.2;
    }

    .brand-subtitle {
      font-size: 12px;
      color: var(--text-secondary);
      font-weight: 500;
    }

    .header-center {
      display: flex;
      align-items: center;
      gap: 20px;
    }

    .live-badge-chip {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 20px;
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: #34d399;
      font-weight: 600;
      font-size: 12px;
      letter-spacing: 0.3px;
    }

    .live-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 8px #10b981;
    }

    .header-meta-item {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      color: var(--text-secondary);
    }
    .header-meta-item strong {
      color: var(--text-white);
      font-weight: 600;
    }

    .header-divider {
      width: 1px;
      height: 18px;
      background: var(--border-subtle);
    }

    .header-right {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .health-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 13px;
      color: #94a3b8;
    }
    .health-pill .dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #10b981;
    }

    /* ==========================================================================
       MAIN APP WORKSPACE
       ========================================================================== */
    .app-workspace {
      display: flex;
      height: calc(100vh - 64px);
      width: 100vw;
      position: relative;
    }

    /* ==========================================================================
       LEFT PANEL: CONTROLS & ACTIVE STORMS
       ========================================================================== */
    .left-panel {
      width: 310px;
      min-width: 310px;
      background: var(--bg-panel-solid);
      border-right: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      gap: 20px;
      padding: 20px 18px;
      z-index: 500;
      overflow-y: auto;
    }

    .panel-section-title {
      font-family: var(--font-display);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.6px;
      text-transform: uppercase;
      color: var(--text-secondary);
      margin-bottom: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    /* Forecast Horizon Button Grid */
    .horizon-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 6px;
    }

    .horizon-btn {
      background: var(--bg-panel-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 8px 4px;
      text-align: center;
      font-family: var(--font-display);
      font-size: 12px;
      font-weight: 600;
      color: var(--text-secondary);
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .horizon-btn:hover {
      background: var(--bg-panel-hover);
      color: var(--text-white);
      border-color: var(--border-medium);
    }
    .horizon-btn.active {
      background: #0284c7;
      border-color: #38bdf8;
      color: #ffffff;
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4);
    }

    /* Layer Toggles */
    .layers-list {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .layer-card {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-panel-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 10px 12px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .layer-card:hover {
      background: var(--bg-panel-hover);
      border-color: var(--border-medium);
    }
    .layer-card.active {
      border-color: rgba(56, 189, 248, 0.3);
    }

    .layer-leading {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .layer-icon-badge {
      width: 28px;
      height: 28px;
      border-radius: 6px;
      background: rgba(255, 255, 255, 0.05);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
    }

    .layer-title {
      font-size: 13.5px;
      font-weight: 600;
      color: var(--text-white);
    }

    .toggle-switch {
      width: 36px;
      height: 20px;
      background: #334155;
      border-radius: 10px;
      position: relative;
      transition: background 0.2s;
    }
    .toggle-switch::after {
      content: "";
      position: absolute;
      top: 2px;
      left: 2px;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: #ffffff;
      transition: transform 0.2s;
    }
    .layer-card.active .toggle-switch {
      background: #0284c7;
    }
    .layer-card.active .toggle-switch::after {
      transform: translateX(16px);
    }

    /* Active Storms List */
    .storms-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .storm-item-card {
      background: var(--bg-panel-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 12px 14px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .storm-item-card:hover {
      background: var(--bg-panel-hover);
      border-color: var(--border-medium);
    }
    .storm-item-card.selected {
      border-color: var(--red-severe);
      background: rgba(239, 68, 68, 0.08);
      box-shadow: 0 4px 16px rgba(239, 68, 68, 0.2);
    }

    .storm-item-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 4px;
    }

    .storm-item-name {
      font-family: var(--font-display);
      font-size: 15px;
      font-weight: 700;
      color: var(--text-white);
    }

    .storm-badge-pill {
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      letter-spacing: 0.3px;
    }
    .badge-severe {
      background: rgba(239, 68, 68, 0.2);
      color: #f87171;
      border: 1px solid rgba(239, 68, 68, 0.4);
    }
    .badge-elevated {
      background: rgba(245, 158, 11, 0.2);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.4);
    }

    .storm-item-desc {
      font-size: 12px;
      color: var(--text-secondary);
    }

    /* ==========================================================================
       CENTER HERO: THE MAP (HERO ~70% OF VIEWPORT)
       ========================================================================== */
    .center-map-viewport {
      flex: 1;
      height: 100%;
      position: relative;
      background: #060b13;
    }

    #heroVajraMap {
      width: 100%;
      height: 100%;
      background: #060b13;
    }

    /* Floating Mode Toggle (Observed vs Nowcast) */
    .map-mode-pill-bar {
      position: absolute;
      top: 18px;
      left: 18px;
      z-index: 1000;
      background: rgba(14, 21, 37, 0.92);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-medium);
      border-radius: 8px;
      padding: 4px;
      display: flex;
      gap: 4px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
    }

    .map-mode-pill-btn {
      background: none;
      border: none;
      color: var(--text-secondary);
      font-family: var(--font-display);
      font-size: 12px;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .map-mode-pill-btn:hover { color: var(--text-white); }
    .map-mode-pill-btn.active {
      background: #0284c7;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(2, 132, 199, 0.5);
    }

    /* Radar Reflectivity Floating Legend */
    .map-radar-legend {
      position: absolute;
      top: 18px;
      right: 18px;
      z-index: 1000;
      background: rgba(14, 21, 37, 0.92);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-medium);
      border-radius: 8px;
      padding: 10px 14px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .legend-top-text {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      font-weight: 600;
      color: var(--text-secondary);
    }

    .legend-gradient-bar {
      width: 220px;
      height: 8px;
      border-radius: 4px;
      background: linear-gradient(to right,
        #06b6d4 0%,
        #3b82f6 20%,
        #10b981 40%,
        #eab308 60%,
        #f97316 75%,
        #ef4444 88%,
        #d946ef 100%
      );
    }

    .legend-labels {
      display: flex;
      justify-content: space-between;
      font-size: 10px;
      color: var(--text-muted);
      font-weight: 500;
    }

    /* ==========================================================================
       BOTTOM FORECAST TIMELINE: POLISHED & CINEMATIC
       ========================================================================== */
    .bottom-timeline-container {
      position: absolute;
      bottom: 24px;
      left: 32px;
      right: 32px;
      z-index: 1000;
      background: rgba(14, 21, 37, 0.95);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-medium);
      border-radius: 12px;
      padding: 14px 22px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 20px;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.7);
    }

    .timeline-playback-action {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .btn-play-forecast {
      background: #0284c7;
      border: none;
      border-radius: 8px;
      padding: 8px 16px;
      color: #ffffff;
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(2, 132, 199, 0.4);
      transition: all 0.15s ease;
    }
    .btn-play-forecast:hover {
      background: #0369a1;
      transform: translateY(-1px);
    }

    .timeline-steps-track {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: relative;
    }

    .timeline-connecting-line {
      position: absolute;
      left: 10px;
      right: 10px;
      height: 3px;
      background: rgba(255, 255, 255, 0.12);
      z-index: 1;
    }

    .timeline-step-node {
      position: relative;
      z-index: 2;
      display: flex;
      flex-direction: column;
      align-items: center;
      cursor: pointer;
      padding: 6px 10px;
      border-radius: 8px;
      transition: all 0.15s ease;
    }
    .timeline-step-node:hover {
      background: rgba(255, 255, 255, 0.08);
    }

    .step-marker-dot {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: #334155;
      border: 2px solid var(--bg-panel-solid);
      margin-bottom: 6px;
      transition: all 0.15s ease;
    }

    .step-label-text {
      font-family: var(--font-display);
      font-size: 12px;
      font-weight: 600;
      color: var(--text-secondary);
      letter-spacing: 0.2px;
    }

    .timeline-step-node.active .step-marker-dot {
      background: #38bdf8;
      box-shadow: 0 0 10px #38bdf8;
      transform: scale(1.3);
    }
    .timeline-step-node.active .step-label-text {
      color: #ffffff;
      font-weight: 700;
    }

    /* ==========================================================================
       RIGHT PANEL: CONTEXTUAL INTELLIGENCE (OPERATOR'S BRIEF)
       ========================================================================== */
    .right-panel {
      width: 380px;
      min-width: 380px;
      background: var(--bg-panel-solid);
      border-left: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      gap: 22px;
      padding: 24px 22px;
      z-index: 500;
      overflow-y: auto;
    }

    /* Cell Header */
    .cell-hero-header {
      display: flex;
      flex-direction: column;
      gap: 6px;
      border-bottom: 1px solid var(--border-subtle);
      padding-bottom: 16px;
    }

    .cell-title-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .cell-hero-title {
      font-family: var(--font-display);
      font-size: 26px;
      font-weight: 800;
      color: var(--text-white);
      letter-spacing: -0.5px;
    }

    .cell-severity-pill {
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.4);
      color: #f87171;
      font-family: var(--font-display);
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .cell-hero-callout {
      font-size: 14px;
      font-weight: 600;
      color: #fca5a5;
    }

    /* 4 Primary Hero Metrics (2x2 Grid) */
    .metrics-2x2-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }

    .hero-metric-card {
      background: var(--bg-panel-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 14px;
      display: flex;
      flex-direction: column;
    }

    .hero-metric-val {
      font-family: var(--font-display);
      font-size: 28px;
      font-weight: 800;
      color: var(--text-white);
      line-height: 1.1;
      letter-spacing: -0.5px;
    }
    .hero-metric-val.val-severe { color: var(--red-severe); }
    .hero-metric-val.val-cyan { color: var(--cyan-obs); }

    .hero-metric-label {
      font-size: 12px;
      color: var(--text-secondary);
      font-weight: 500;
      margin-top: 4px;
    }

    /* Section: WHY IS IT INTENSIFYING? */
    .intel-sub-section {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .intel-sub-title {
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      color: var(--text-secondary);
    }

    .evidence-cards-container {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .evidence-row-card {
      background: var(--bg-panel-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 10px 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 13.5px;
    }

    .evidence-row-card .k-label {
      color: var(--text-primary);
      font-weight: 500;
    }

    .evidence-row-card .v-arrow {
      font-weight: 700;
      color: var(--red-severe);
      display: flex;
      align-items: center;
      gap: 4px;
    }

    /* Section: POTENTIAL IMPACT */
    .impact-metrics-row {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
    }

    .impact-box {
      background: var(--bg-panel-elevated);
      border-left: 3px solid var(--amber-dev);
      border-radius: 0 8px 8px 0;
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
    }

    .impact-number {
      font-family: var(--font-display);
      font-size: 20px;
      font-weight: 800;
      color: var(--text-white);
    }

    .impact-caption {
      font-size: 12px;
      color: var(--text-secondary);
      font-weight: 500;
    }

    /* ==========================================================================
       MAP CUSTOM STYLING (LEAFLET)
       ========================================================================== */
    .leaflet-container {
      background: #080e18 !important;
      font-family: var(--font-body);
    }

    /* Satellite/Dark Tiles Filter for Photographic Beauty */
    .leaflet-tile-pane {
      filter: brightness(0.72) contrast(1.18) saturate(1.12);
    }

    /* Storm Footprint Pulse Marker */
    .storm-core-pulsar {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: rgba(239, 68, 68, 0.45);
      border: 2px solid #ef4444;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #ffffff;
      font-family: var(--font-display);
      font-size: 11px;
      font-weight: 800;
      box-shadow: 0 0 20px rgba(239, 68, 68, 0.8);
      cursor: pointer;
      animation: pulse-core 2s infinite ease-in-out;
    }

    @keyframes pulse-core {
      0%, 100% { transform: scale(1); box-shadow: 0 0 14px rgba(239, 68, 68, 0.7); }
      50% { transform: scale(1.15); box-shadow: 0 0 26px rgba(239, 68, 68, 1); }
    }

    /* Lightning Flash Strobe Marker */
    .lightning-pulse-strobe {
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: #67e8f9;
      box-shadow: 0 0 14px #38bdf8;
      animation: ltg-flash 1.6s infinite ease-out;
    }
    @keyframes ltg-flash {
      0% { transform: scale(0.3); opacity: 1; }
      50% { transform: scale(2.0); opacity: 0.6; }
      100% { transform: scale(3.2); opacity: 0; }
    }

    /* City Label Pill on Map */
    .city-map-badge {
      background: rgba(9, 14, 23, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.18);
      border-radius: 4px;
      padding: 2px 7px;
      font-size: 11px;
      font-weight: 600;
      color: #ffffff;
      white-space: nowrap;
      pointer-events: none;
    }
  </style>
</head>
<body>

  <!-- ==========================================================================
       HEADER: MINIMAL, ELEGANT PRODUCT HEADER
       ========================================================================== -->
  <header class="product-header">
    <div class="header-left">
      <div class="brand-logo-mark">
        <svg viewBox="0 0 24 24">
          <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
        </svg>
      </div>
      <div class="brand-title-wrap">
        <span class="brand-title">VAJRA</span>
        <span class="brand-subtitle">Very-short-term Atmospheric Risk &amp; Joint Analysis</span>
      </div>
    </div>

    <!-- Center System Information -->
    <div class="header-center">
      <div class="live-badge-chip">
        <span class="live-dot"></span>
        <span>LIVE</span>
      </div>

      <div class="header-meta-item">
        <span>Domain:</span>
        <strong>India (Eastern Sector)</strong>
      </div>

      <div class="header-divider"></div>

      <div class="header-meta-item">
        <span>Freshness:</span>
        <strong id="headerFreshness">Updated 2m ago</strong>
      </div>

      <div class="header-divider"></div>

      <div class="header-meta-item">
        <span>Model Status:</span>
        <strong>Radar + Satellite AI (Ensemble)</strong>
      </div>
    </div>

    <!-- Right Quick Telemetry -->
    <div class="header-right">
      <div class="header-meta-item">
        <span>Horizon:</span>
        <strong id="headerHorizonLabel">Nowcasting to +2h</strong>
      </div>

      <div class="header-divider"></div>

      <div class="health-pill">
        <span class="dot"></span>
        <span>All Systems Active</span>
      </div>
    </div>
  </header>

  <!-- ==========================================================================
       MAIN WORKSPACE: LEFT CONTROLS | MAP (HERO) | RIGHT INTELLIGENCE
       ========================================================================== -->
  <main class="app-workspace">

    <!-- LEFT PANEL: FORECAST HORIZON, LAYERS, ACTIVE STORMS -->
    <aside class="left-panel">
      <!-- Forecast Horizon Buttons -->
      <div>
        <div class="panel-section-title">
          <span>FORECAST</span>
          <span style="color:var(--cyan-obs); font-weight:600;" id="horizonIndicator">+30 MIN</span>
        </div>
        <div class="horizon-grid">
          <button class="horizon-btn" data-min="15">15 MIN</button>
          <button class="horizon-btn active" data-min="30">30 MIN</button>
          <button class="horizon-btn" data-min="60">1 HR</button>
          <button class="horizon-btn" data-min="120">2 HR</button>
          <button class="horizon-btn" data-min="180">3 HR</button>
          <button class="horizon-btn" data-min="360">6 HR</button>
        </div>
      </div>

      <!-- Atmospheric Layers -->
      <div>
        <div class="panel-section-title">
          <span>LAYERS</span>
        </div>
        <div class="layers-list">
          <div class="layer-card active" id="layerToggleRadar">
            <div class="layer-leading">
              <div class="layer-icon-badge">📡</div>
              <span class="layer-title">Radar</span>
            </div>
            <div class="toggle-switch"></div>
          </div>

          <div class="layer-card active" id="layerToggleSat">
            <div class="layer-leading">
              <div class="layer-icon-badge">🛰</div>
              <span class="layer-title">Satellite</span>
            </div>
            <div class="toggle-switch"></div>
          </div>

          <div class="layer-card active" id="layerToggleLtg">
            <div class="layer-leading">
              <div class="layer-icon-badge">⚡</div>
              <span class="layer-title">Lightning</span>
            </div>
            <div class="toggle-switch"></div>
          </div>

          <div class="layer-card active" id="layerToggleTracks">
            <div class="layer-leading">
              <div class="layer-icon-badge">↗</div>
              <span class="layer-title">Storm Tracks</span>
            </div>
            <div class="toggle-switch"></div>
          </div>

          <div class="layer-card active" id="layerToggleInfra">
            <div class="layer-leading">
              <div class="layer-icon-badge">🏢</div>
              <span class="layer-title">Infrastructure</span>
            </div>
            <div class="toggle-switch"></div>
          </div>
        </div>
      </div>

      <!-- Active Storms List -->
      <div style="flex:1;">
        <div class="panel-section-title">
          <span>ACTIVE STORMS</span>
          <span style="color:var(--red-severe);">2 TRACKED</span>
        </div>
        <div class="storms-list">
          <!-- Storm Cell 024 -->
          <div class="storm-item-card selected" id="stormCard024" onclick="selectStorm('024')">
            <div class="storm-item-header">
              <span class="storm-item-name">Storm Cell 024</span>
              <span class="storm-badge-pill badge-severe">68 dBZ</span>
            </div>
            <div class="storm-item-desc">Rapidly intensifying &bull; ENE 34 km/h</div>
          </div>

          <!-- Storm Cell 018 -->
          <div class="storm-item-card" id="stormCard018" onclick="selectStorm('018')">
            <div class="storm-item-header">
              <span class="storm-item-name">Storm Cell 018</span>
              <span class="storm-badge-pill badge-elevated">52 dBZ</span>
            </div>
            <div class="storm-item-desc">Moving east &bull; E 28 km/h</div>
          </div>
        </div>
      </div>
    </aside>

    <!-- CENTER HERO MAP (~70% VIEWPORT HERO) -->
    <section class="center-map-viewport">
      <div id="heroVajraMap"></div>

      <!-- Observed vs AI Nowcast Pill Toggle -->
      <div class="map-mode-pill-bar">
        <button class="map-mode-pill-btn" id="btnModeObserved">OBSERVED</button>
        <button class="map-mode-pill-btn active" id="btnModeNowcast">AI NOWCAST</button>
      </div>

      <!-- Radar Reflectivity Legend -->
      <div class="map-radar-legend">
        <div class="legend-top-text">
          <span>COMPOSITE REFLECTIVITY</span>
          <span style="color:var(--red-severe);">HAIL &gt; 55 dBZ</span>
        </div>
        <div class="legend-gradient-bar"></div>
        <div class="legend-labels">
          <span>15</span>
          <span>25</span>
          <span>35</span>
          <span>45</span>
          <span>55</span>
          <span>65+ dBZ</span>
        </div>
      </div>

      <!-- BOTTOM FORECAST TIMELINE -->
      <div class="bottom-timeline-container">
        <div class="timeline-playback-action">
          <button class="btn-play-forecast" id="btnPlayForecast">
            <span id="playIcon">▶</span>
            <span id="playText">PLAY FORECAST</span>
          </button>
        </div>

        <div class="timeline-steps-track">
          <div class="timeline-connecting-line"></div>

          <div class="timeline-step-node" data-step="0">
            <div class="step-marker-dot"></div>
            <span class="step-label-text">NOW</span>
          </div>

          <div class="timeline-step-node" data-step="1">
            <div class="step-marker-dot"></div>
            <span class="step-label-text">+15</span>
          </div>

          <div class="timeline-step-node active" data-step="2">
            <div class="step-marker-dot"></div>
            <span class="step-label-text">+30</span>
          </div>

          <div class="timeline-step-node" data-step="3">
            <div class="step-marker-dot"></div>
            <span class="step-label-text">+45</span>
          </div>

          <div class="timeline-step-node" data-step="4">
            <div class="step-marker-dot"></div>
            <span class="step-label-text">+60</span>
          </div>

          <div class="timeline-step-node" data-step="5">
            <div class="step-marker-dot"></div>
            <span class="step-label-text">+90</span>
          </div>

          <div class="timeline-step-node" data-step="6">
            <div class="step-marker-dot"></div>
            <span class="step-label-text">+120</span>
          </div>
        </div>
      </div>
    </section>

    <!-- RIGHT PANEL: CONTEXTUAL INTELLIGENCE PANEL (OPERATOR'S BRIEF) -->
    <aside class="right-panel">
      <!-- Selected Storm Header -->
      <div class="cell-hero-header">
        <div class="cell-title-row">
          <span class="cell-hero-title" id="intelStormTitle">STORM CELL 024</span>
          <span class="cell-severity-pill" id="intelStormPill">SEVERE</span>
        </div>
        <div class="cell-hero-callout" id="intelStormCallout">RAPIDLY INTENSIFYING</div>
      </div>

      <!-- 4 Primary Metrics (2x2 Grid) -->
      <div class="metrics-2x2-grid">
        <div class="hero-metric-card">
          <span class="hero-metric-val val-severe" id="metricDbz">68 dBZ</span>
          <span class="hero-metric-label">Current intensity</span>
        </div>

        <div class="hero-metric-card">
          <span class="hero-metric-val" id="metricSpeed">34 km/h</span>
          <span class="hero-metric-label" id="metricDirection">Moving southeast</span>
        </div>

        <div class="hero-metric-card">
          <span class="hero-metric-val val-cyan" id="metricEta">18–27 min</span>
          <span class="hero-metric-label">Estimated arrival</span>
        </div>

        <div class="hero-metric-card">
          <span class="hero-metric-val" id="metricConfidence">87%</span>
          <span class="hero-metric-label">Forecast confidence</span>
        </div>
      </div>

      <!-- WHY IS IT INTENSIFYING? -->
      <div class="intel-sub-section">
        <span class="intel-sub-title">WHY IS IT INTENSIFYING?</span>
        <div class="evidence-cards-container">
          <div class="evidence-row-card">
            <span class="k-label">Radar growth</span>
            <span class="v-arrow" id="evRadar">↑ Rapid (+14 dBZ/15m)</span>
          </div>
          <div class="evidence-row-card">
            <span class="k-label">Lightning activity</span>
            <span class="v-arrow" id="evLtg">↑ Severe (58 /min)</span>
          </div>
          <div class="evidence-row-card">
            <span class="k-label">Cloud development</span>
            <span class="v-arrow" id="evCloud">↑ Overshooting top (15.2 km)</span>
          </div>
          <div class="evidence-row-card">
            <span class="k-label">Instability</span>
            <span class="v-arrow" id="evCape" style="color:#f59e0b;">HIGH (SBCAPE 3,650 J/kg)</span>
          </div>
        </div>
      </div>

      <!-- POTENTIAL IMPACT -->
      <div class="intel-sub-section">
        <span class="intel-sub-title">POTENTIAL IMPACT</span>
        <div class="impact-metrics-row">
          <div class="impact-box">
            <span class="impact-number" id="impAirports">01</span>
            <span class="impact-caption">Airport (VECC Kolkata)</span>
          </div>
          <div class="impact-box">
            <span class="impact-number" id="impRoads">08</span>
            <span class="impact-caption">Major roads (NH-16, NH-19)</span>
          </div>
          <div class="impact-box">
            <span class="impact-number" id="impPower">14</span>
            <span class="impact-caption">Power assets (765kV Grid)</span>
          </div>
          <div class="impact-box">
            <span class="impact-number" id="impPop">182K</span>
            <span class="impact-caption">Population in corridor</span>
          </div>
        </div>
      </div>
    </aside>
  </main>

  <!-- ==========================================================================
       GEOSPATIAL ENGINE & INTERACTIVE LOGIC
       ========================================================================== -->
  <script>
    /* ==========================================================================
       1. DATA STRUCTURES & DEFINITIONS
       ========================================================================== */
    const STORM_DATA = {
      '024': {
        id: 'STORM CELL 024',
        pill: 'SEVERE',
        callout: 'RAPIDLY INTENSIFYING',
        dbz: '68 dBZ',
        speed: '34 km/h',
        direction: 'Moving southeast',
        eta: '18–27 min',
        confidence: '87%',
        why: {
          radar: '↑ Rapid (+14 dBZ/15m)',
          ltg: '↑ Severe (58 /min)',
          cloud: '↑ Overshooting top (15.2 km)',
          cape: 'HIGH (SBCAPE 3,650 J/kg)'
        },
        impact: {
          airports: '01',
          roads: '08',
          power: '14',
          pop: '182K'
        },
        center: [22.62, 88.20],
        // Trajectory points: NOW, +15m, +30m, +45m, +60m, +90m, +120m
        track: [
          [22.42, 87.85], // NOW
          [22.51, 88.08], // +15
          [22.60, 88.32], // +30
          [22.68, 88.54], // +45
          [22.76, 88.76], // +60
          [22.88, 89.10], // +90
          [23.00, 89.45]  // +120
        ],
        lightnings: [
          [22.44, 87.87], [22.41, 87.82], [22.47, 87.92],
          [22.39, 87.80], [22.45, 87.94]
        ]
      },
      '018': {
        id: 'STORM CELL 018',
        pill: 'ELEVATED',
        callout: 'STEADY FORWARD ADVECTION',
        dbz: '52 dBZ',
        speed: '28 km/h',
        direction: 'Moving east',
        eta: '35–45 min',
        confidence: '82%',
        why: {
          radar: '→ Steady (+3 dBZ/15m)',
          ltg: '↑ Moderate (24 /min)',
          cloud: '→ High cirrus top (13.0 km)',
          cape: 'MODERATE (2,400 J/kg)'
        },
        impact: {
          airports: '00',
          roads: '04',
          power: '06',
          pop: '94K'
        },
        center: [23.25, 88.10],
        track: [
          [23.24, 87.88], // NOW
          [23.28, 88.14], // +15
          [23.32, 88.38], // +30
          [23.36, 88.62], // +45
          [23.40, 88.86], // +60
          [23.46, 89.18], // +90
          [23.52, 89.50]  // +120
        ],
        lightnings: [
          [23.22, 87.85], [23.26, 87.91], [23.25, 87.89]
        ]
      }
    };

    let activeStormId = '024';
    let currentStep = 2; // Default +30 min
    let currentMode = 'nowcast'; // 'observed' or 'nowcast'
    let isPlaying = false;
    let playInterval = null;

    // Map object & layer groups
    let map = null;
    let layerRadar = null;
    let layerSat = null;
    let layerLtg = null;
    let layerTracks = null;
    let layerInfra = null;

    /* ==========================================================================
       2. INITIALIZATION
       ========================================================================== */
    window.addEventListener('DOMContentLoaded', () => {
      initMap();
      setupUIEvents();
      renderAllMapFeatures();
    });

    /* ==========================================================================
       3. LEAFLET MAP INITIALIZATION WITH ROBUST FALLBACK
       ========================================================================== */
    function initMap() {
      // Create Leaflet map centered over Eastern India
      map = L.map('heroVajraMap', {
        zoomControl: false,
        attributionControl: false,
        preferCanvas: true
      }).setView([22.65, 88.25], 8);

      L.control.zoom({ position: 'topright' }).addTo(map);

      // Primary High-Definition Satellite / Dark Hybrid Basemap
      // Using Esri World Imagery with Carto Dark Fallback
      const esriSatellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 18,
        opacity: 0.85
      });

      const osmFallback = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        opacity: 0.35
      });

      esriSatellite.addTo(map);
      osmFallback.addTo(map);

      // Dedicated Layer Groups
      layerRadar = L.layerGroup().addTo(map);
      layerSat = L.layerGroup().addTo(map);
      layerLtg = L.layerGroup().addTo(map);
      layerTracks = L.layerGroup().addTo(map);
      layerInfra = L.layerGroup().addTo(map);

      // Add geographic city markers for immediate spatial orientation
      addGeographicContext();
    }

    /* Add recognizable Indian cities and terrain context */
    function addGeographicContext() {
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
          className: 'city-label-icon',
          html: `<div class="city-map-badge">${c.name}</div>`,
          iconSize: [60, 20],
          iconAnchor: [30, 10]
        });
        L.marker([c.lat, c.lon], { icon: badge, interactive: false }).addTo(layerInfra);
      });
    }

    /* ==========================================================================
       4. SIGNATURE STORM VISUALIZATION: SHADOW, CORRIDOR & TRACK
       ========================================================================== */
    function renderAllMapFeatures() {
      layerRadar.clearLayers();
      layerLtg.clearLayers();
      layerTracks.clearLayers();

      const activeStorm = STORM_DATA[activeStormId];
      const track = activeStorm.track;

      // 1. UNCERTAINTY CORRIDOR (Broadening corridor downwind)
      if (currentMode === 'nowcast') {
        const p0 = track[0];
        const pTarget = track[currentStep] || track[track.length - 1];
        const expandFactor = 0.08 + (currentStep * 0.05);

        const corridorCoords = [
          [p0[0], p0[1]],
          [pTarget[0] + expandFactor * 0.7, pTarget[1] - expandFactor],
          [pTarget[0] + expandFactor, pTarget[1] + expandFactor],
          [pTarget[0] - expandFactor * 0.5, pTarget[1] + expandFactor * 0.8],
          [p0[0], p0[1]]
        ];

        L.polygon(corridorCoords, {
          color: '#a855f7',
          fillColor: '#a855f7',
          fillOpacity: 0.12,
          weight: 1.5,
          dashArray: '4, 6'
        }).addTo(layerTracks);
      }

      // 2. STORM TRAJECTORY (Smooth connecting line)
      L.polyline(track, {
        color: '#38bdf8',
        weight: 3,
        opacity: 0.9,
        dashArray: '6, 6'
      }).addTo(layerTracks);

      // 3. CURRENT STORM FOOTPRINT (Prominent, rich multi-tier radar Doppler cores)
      const t0 = track[0];
      // Outer precipitation footprint (35 dBZ)
      L.circle(t0, {
        radius: 22000,
        color: '#10b981',
        fillColor: '#10b981',
        fillOpacity: 0.28,
        weight: 1
      }).addTo(layerRadar);

      // Elevated convective band (50 dBZ)
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
        color: '#ef4444',
        fillColor: '#ef4444',
        fillOpacity: 0.8,
        weight: 2
      }).addTo(layerRadar);

      // 4. STORM SHADOW (Future storm positions appear as increasingly translucent footprints!)
      if (currentMode === 'nowcast') {
        const stepLabels = ['NOW', '+15m', '+30m', '+45m', '+60m', '+90m', '+120m'];

        for (let i = 1; i <= currentStep; i++) {
          const pt = track[i];
          if (!pt) continue;

          // Translucency fades progressively into the distance
          const shadowOpacity = Math.max(0.12, 0.48 - (i * 0.07));
          const shadowRadius = 18000 + (i * 2200);

          L.circle(pt, {
            radius: shadowRadius,
            color: '#f97316',
            fillColor: '#f97316',
            fillOpacity: shadowOpacity,
            weight: 1,
            dashArray: '3, 4'
          }).addTo(layerRadar);

          // Subtle Waypoint marker
          L.circleMarker(pt, {
            radius: 5,
            color: '#38bdf8',
            fillColor: '#090e17',
            fillOpacity: 1,
            weight: 2
          }).bindTooltip(`${stepLabels[i]} position (${activeStorm.id})`, {
            permanent: false
          }).addTo(layerTracks);
        }
      }

      // 5. ACTIVE STORM CORE MARKER
      const activeCentroid = (currentMode === 'nowcast' && currentStep > 0) ? track[currentStep] : t0;
      const coreIcon = L.divIcon({
        className: 'core-marker-wrap',
        html: `<div class="storm-core-pulsar" title="${activeStorm.id}">${parseInt(activeStorm.dbz)}</div>`,
        iconSize: [32, 32],
        iconAnchor: [16, 16]
      });

      L.marker(activeCentroid, { icon: coreIcon }).addTo(layerTracks);

      // 6. LIGHTNING ACTIVITY (Electric pulse density)
      activeStorm.lightnings.forEach(lt => {
        const ltIcon = L.divIcon({
          className: 'lt-icon-wrap',
          html: '<div class="lightning-pulse-strobe"></div>',
          iconSize: [14, 14],
          iconAnchor: [7, 7]
        });
        L.marker(lt, { icon: ltIcon }).addTo(layerLtg);
      });

      // 7. CRITICAL INFRASTRUCTURE ICONS (Airport & Grid)
      const airports = [
        { name: "VECC (Kolkata Airport)", pt: [22.654, 88.446], alert: true },
        { name: "765kV Regional Substation", pt: [22.42, 87.35], alert: true }
      ];

      airports.forEach(a => {
        L.circleMarker(a.pt, {
          radius: 7,
          color: a.alert ? '#ef4444' : '#38bdf8',
          fillColor: a.alert ? '#ef4444' : '#090e17',
          fillOpacity: 0.9,
          weight: 2
        }).bindTooltip(`${a.name} [ALERT]`, { permanent: false }).addTo(layerTracks);
      });
    }

    /* ==========================================================================
       5. SELECT STORM CELL (INTERACTION & RIGHT PANEL UPDATE)
       ========================================================================== */
    function selectStorm(stormId) {
      activeStormId = stormId;
      const data = STORM_DATA[stormId];

      // Update card selections in left panel
      document.querySelectorAll('.storm-item-card').forEach(c => c.classList.remove('selected'));
      const activeCard = document.getElementById(`stormCard${stormId}`);
      if (activeCard) activeCard.classList.add('selected');

      // Update Right Panel Contextual Intelligence
      document.getElementById('intelStormTitle').textContent = data.id;
      document.getElementById('intelStormPill').textContent = data.pill;
      document.getElementById('intelStormCallout').textContent = data.callout;

      document.getElementById('metricDbz').textContent = data.dbz;
      document.getElementById('metricSpeed').textContent = data.speed;
      document.getElementById('metricDirection').textContent = data.direction;
      document.getElementById('metricEta').textContent = data.eta;
      document.getElementById('metricConfidence').textContent = data.confidence;

      document.getElementById('evRadar').textContent = data.why.radar;
      document.getElementById('evLtg').textContent = data.why.ltg;
      document.getElementById('evCloud').textContent = data.why.cloud;
      document.getElementById('evCape').textContent = data.why.cape;

      document.getElementById('impAirports').textContent = data.impact.airports;
      document.getElementById('impRoads').textContent = data.impact.roads;
      document.getElementById('impPower').textContent = data.impact.power;
      document.getElementById('impPop').textContent = data.impact.pop;

      // Pan map smoothly to the storm
      map.flyTo(data.center, 8, { duration: 0.8 });

      // Re-render storm shadows and corridors
      renderAllMapFeatures();
    }

    /* ==========================================================================
       6. TIMELINE CONTROLS & PLAYBACK
       ========================================================================== */
    function setTimelineStep(stepIdx) {
      currentStep = stepIdx;

      // Update timeline step node UI
      const nodes = document.querySelectorAll('.timeline-step-node');
      nodes.forEach((n, idx) => {
        n.classList.toggle('active', idx === stepIdx);
      });

      const horizonLabels = ['NOW', '+15 MIN', '+30 MIN', '+45 MIN', '+60 MIN', '+90 MIN', '+120 MIN'];
      document.getElementById('horizonIndicator').textContent = horizonLabels[stepIdx];
      document.getElementById('headerHorizonLabel').textContent = `Nowcasting to ${horizonLabels[stepIdx]}`;

      renderAllMapFeatures();
    }

    /* ==========================================================================
       7. UI EVENT HANDLERS
       ========================================================================== */
    function setupUIEvents() {
      // Forecast Horizon Buttons in Left Panel
      const hMap = { 15: 1, 30: 2, 60: 4, 120: 6, 180: 6, 360: 6 };
      document.querySelectorAll('.horizon-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          document.querySelectorAll('.horizon-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          const min = parseInt(btn.dataset.min);
          setTimelineStep(hMap[min] || 2);
        });
      });

      // Bottom Timeline Step Nodes
      document.querySelectorAll('.timeline-step-node').forEach(node => {
        node.addEventListener('click', () => {
          const step = parseInt(node.dataset.step);
          setTimelineStep(step);
        });
      });

      // Play / Pause Forecast Playback
      const playBtn = document.getElementById('btnPlayForecast');
      const playIcon = document.getElementById('playIcon');
      const playText = document.getElementById('playText');

      playBtn.addEventListener('click', () => {
        isPlaying = !isPlaying;
        if (isPlaying) {
          playIcon.textContent = '⏸';
          playText.textContent = 'PAUSE FORECAST';
          playInterval = setInterval(() => {
            let nextStep = (currentStep + 1) % 7;
            setTimelineStep(nextStep);
          }, 1500);
        } else {
          playIcon.textContent = '▶';
          playText.textContent = 'PLAY FORECAST';
          clearInterval(playInterval);
        }
      });

      // Observed vs AI Nowcast Modes
      document.getElementById('btnModeObserved').addEventListener('click', () => {
        currentMode = 'observed';
        document.getElementById('btnModeObserved').classList.add('active');
        document.getElementById('btnModeNowcast').classList.remove('active');
        renderAllMapFeatures();
      });

      document.getElementById('btnModeNowcast').addEventListener('click', () => {
        currentMode = 'nowcast';
        document.getElementById('btnModeNowcast').classList.add('active');
        document.getElementById('btnModeObserved').classList.remove('active');
        renderAllMapFeatures();
      });

      // Layer Toggles
      const setupLayerCard = (cardId, layerObj) => {
        const card = document.getElementById(cardId);
        card.addEventListener('click', () => {
          card.classList.toggle('active');
          if (card.classList.contains('active')) {
            map.addLayer(layerObj);
          } else {
            map.removeLayer(layerObj);
          }
        });
      };

      setupLayerCard('layerToggleRadar', layerRadar);
      setupLayerCard('layerToggleSat', layerSat);
      setupLayerCard('layerToggleLtg', layerLtg);
      setupLayerCard('layerToggleTracks', layerTracks);
      setupLayerCard('layerToggleInfra', layerInfra);
    }
  </script>
</body>
</html>
"""

with open("dashboard/index.html", "w", encoding="utf-8") as f:
    f.write(html_code)

print(f"Written ground-up redesigned VAJRA dashboard: {len(html_code)} bytes")
