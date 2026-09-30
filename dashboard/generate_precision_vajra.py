# -*- coding: utf-8 -*-
"""
VAJRA Precision Command Center Generator
Strictly adhering to specifications:
- Thin status bar (VAJRA, Live Atmospheric Intelligence, Data freshness, Model status, Last obs, Horizon, System health)
- Compact Left Intelligence Rail (Active Threats, Forecast Horizon, Layers, Playback)
- Center Hero Map with Storm Shadow (progressive translucency), Uncertainty Corridor expansion, and Observed vs Nowcast toggle
- Right Contextual Intelligence Panel (Storm Cell #024, Rapidly Intensifying, Telemetry, Threat, WHY NOW evidence, WHAT IS AT RISK)
- Bottom Forecast Timeline (NOW, +15, +30, +45, +60, +90, +120 MIN)
"""

html_code = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>VAJRA — Live Atmospheric Intelligence Command Center</title>
  <meta name="description" content="VAJRA: Atmospheric Intelligence Command Center. AIML-based Nowcasting of Thunderstorm and Lightning over India." />

  <!-- Fonts: Space Grotesk, Inter, IBM Plex Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet" />

  <!-- Leaflet CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

  <style>
    /* ==========================================================================
       TACTICAL DESIGN TOKENS
       ========================================================================== */
    :root {
      --bg-void: #04070d;
      --bg-base: #070b14;
      --bg-panel: #0a0f1b;
      --bg-panel-elevated: #0f1626;
      --bg-panel-hover: #141d33;
      --bg-field: #080d18;

      --border-subtle: rgba(255, 255, 255, 0.06);
      --border-line: rgba(255, 255, 255, 0.1);
      --border-active: rgba(56, 189, 248, 0.3);

      --text-pure: #ffffff;
      --text-bright: #e2e8f0;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --text-faint: #475569;

      /* Semantic Radar & Warning Palette */
      --cyan-obs: #38bdf8;
      --amber-dev: #f59e0b;
      --orange-elev: #f97316;
      --red-severe: #ef4444;
      --purple-uncert: #c084fc;
      --green-stable: #10b981;

      --font-brand: 'Space Grotesk', sans-serif;
      --font-body: 'Inter', -apple-system, sans-serif;
      --font-mono: 'IBM Plex Mono', monospace;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }

    body {
      background: var(--bg-void);
      color: var(--text-bright);
      font-family: var(--font-body);
      font-size: 12px;
      line-height: 1.4;
      height: 100vh;
      width: 100vw;
      overflow: hidden;
      user-select: none;
    }

    /* Scrollbars */
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: var(--bg-void); }
    ::-webkit-scrollbar-thumb { background: #1a2336; border-radius: 2px; }

    /* ==========================================================================
       TOP: REFINED THIN STATUS / SYSTEM BAR
       ========================================================================== */
    .thin-status-bar {
      height: 38px;
      background: var(--bg-base);
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 14px;
      z-index: 1000;
      font-family: var(--font-mono);
      font-size: 11px;
    }

    .status-left-brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .brand-mark {
      font-family: var(--font-brand);
      font-size: 15px;
      font-weight: 700;
      letter-spacing: 2px;
      color: var(--text-pure);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .brand-tag {
      font-size: 8.5px;
      letter-spacing: 1px;
      padding: 1px 5px;
      border: 1px solid var(--border-active);
      color: var(--cyan-obs);
      border-radius: 2px;
      background: rgba(56, 189, 248, 0.08);
      font-weight: 600;
    }

    .brand-subtitle {
      font-size: 9.5px;
      color: var(--text-dim);
      letter-spacing: 0.8px;
      font-family: var(--font-mono);
      text-transform: uppercase;
    }

    .status-telemetry-cluster {
      display: flex;
      align-items: center;
      gap: 18px;
    }

    .telemetry-item {
      display: flex;
      align-items: center;
      gap: 5px;
    }

    .telemetry-lbl {
      color: var(--text-dim);
      font-size: 9px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .telemetry-val {
      color: var(--text-bright);
      font-weight: 600;
      font-size: 10.5px;
    }

    .telemetry-dot {
      width: 5px;
      height: 5px;
      border-radius: 50%;
      background: var(--green-stable);
      box-shadow: 0 0 5px var(--green-stable);
    }
    .telemetry-dot.pulse {
      animation: pulse-dot 1.8s infinite ease-in-out;
    }
    @keyframes pulse-dot {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(1.3); }
    }

    .status-right-tools {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .clock-ticker {
      font-size: 11px;
      font-weight: 600;
      color: var(--text-pure);
      letter-spacing: 0.5px;
    }

    .btn-status-pill {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 2px;
      padding: 3px 8px;
      font-family: var(--font-mono);
      font-size: 9.5px;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
      transition: all 0.15s;
    }
    .btn-status-pill:hover {
      border-color: var(--border-active);
      color: var(--text-pure);
    }
    .btn-status-pill.active {
      border-color: var(--cyan-obs);
      color: var(--cyan-obs);
      background: rgba(56, 189, 248, 0.08);
    }

    /* ==========================================================================
       MAIN COMMAND CENTER WORKSPACE
       ========================================================================== */
    .command-workspace {
      display: flex;
      height: calc(100vh - 38px);
      width: 100vw;
      position: relative;
    }

    /* ==========================================================================
       LEFT: COMPACT INTELLIGENCE & CONTROL RAIL
       ========================================================================== */
    .left-intel-rail {
      width: 260px;
      min-width: 260px;
      background: var(--bg-base);
      border-right: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      z-index: 500;
      overflow-y: auto;
    }

    .rail-section {
      padding: 10px 12px;
      border-bottom: 1px solid var(--border-subtle);
    }

    .rail-section-header {
      font-family: var(--font-mono);
      font-size: 9.5px;
      font-weight: 700;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      color: var(--text-dim);
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .rail-section-header .metric-badge {
      color: var(--cyan-obs);
      font-size: 8.5px;
    }

    /* Active Threats Summary Card */
    .threat-stat-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
    }

    .threat-stat-box {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 2px;
      padding: 6px 8px;
      display: flex;
      flex-direction: column;
    }

    .threat-stat-box .t-k {
      font-family: var(--font-mono);
      font-size: 8.5px;
      color: var(--text-dim);
      text-transform: uppercase;
    }
    .threat-stat-box .t-v {
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 700;
      color: var(--text-pure);
      margin-top: 1px;
    }
    .threat-stat-box .t-v.severe { color: var(--red-severe); }
    .threat-stat-box .t-v.elevated { color: var(--orange-elev); }

    /* Compact Layer Toggles (Professional Mission Console) */
    .layer-toggle-group {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .layer-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 5px 8px;
      background: var(--bg-panel);
      border: 1px solid transparent;
      border-radius: 2px;
      cursor: pointer;
      transition: background 0.15s;
    }
    .layer-row:hover {
      background: var(--bg-panel-hover);
    }
    .layer-row.active {
      border-color: rgba(255, 255, 255, 0.08);
    }

    .layer-info {
      display: flex;
      align-items: center;
      gap: 7px;
    }

    .layer-indicator {
      width: 6px;
      height: 6px;
      border-radius: 1px;
      background: var(--text-dim);
    }
    .layer-row.active .layer-indicator.c-radar { background: var(--orange-elev); box-shadow: 0 0 5px var(--orange-elev); }
    .layer-row.active .layer-indicator.c-sat { background: #60a5fa; box-shadow: 0 0 5px #60a5fa; }
    .layer-row.active .layer-indicator.c-ltg { background: var(--cyan-obs); box-shadow: 0 0 5px var(--cyan-obs); }
    .layer-row.active .layer-indicator.c-cell { background: var(--red-severe); box-shadow: 0 0 5px var(--red-severe); }
    .layer-row.active .layer-indicator.c-infra { background: #e2e8f0; }
    .layer-row.active .layer-indicator.c-pop { background: var(--purple-uncert); }

    .layer-name {
      font-size: 11px;
      font-weight: 500;
      color: var(--text-bright);
    }

    .layer-sub {
      font-family: var(--font-mono);
      font-size: 8.5px;
      color: var(--text-dim);
    }

    /* Scenario Selector for mission simulation */
    .tactical-select {
      width: 100%;
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 2px;
      color: var(--text-bright);
      padding: 5px 8px;
      font-family: var(--font-mono);
      font-size: 10px;
      outline: none;
      cursor: pointer;
    }
    .tactical-select:focus {
      border-color: var(--border-active);
    }

    /* ==========================================================================
       CENTER HERO: LIVE GEOSPATIAL MAP
       ========================================================================== */
    .center-hero-map {
      flex: 1;
      height: 100%;
      position: relative;
      background: #020408;
    }

    #vajraHeroMap {
      width: 100%;
      height: 100%;
      background: #020408;
    }

    /* Floating Mode Toggle: Observed vs AI Nowcast */
    .map-mode-toggle {
      position: absolute;
      top: 12px;
      left: 12px;
      z-index: 1000;
      background: rgba(7, 11, 20, 0.92);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border-line);
      border-radius: 3px;
      padding: 3px;
      display: flex;
      gap: 3px;
      font-family: var(--font-mono);
      box-shadow: 0 4px 16px rgba(0,0,0,0.7);
    }

    .mode-tab-btn {
      background: none;
      border: none;
      color: var(--text-dim);
      font-size: 10px;
      font-family: var(--font-mono);
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 2px;
      cursor: pointer;
      transition: all 0.15s;
    }
    .mode-tab-btn:hover { color: var(--text-bright); }
    .mode-tab-btn.active {
      background: var(--bg-panel-elevated);
      color: var(--cyan-obs);
      box-shadow: 0 0 8px rgba(56, 189, 248, 0.2);
    }

    /* Radar Reflectivity Ramp Legend Overlay */
    .radar-ramp-bar {
      position: absolute;
      top: 12px;
      right: 12px;
      z-index: 1000;
      background: rgba(7, 11, 20, 0.88);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border-subtle);
      border-radius: 3px;
      padding: 6px 10px;
      font-family: var(--font-mono);
      font-size: 9px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .ramp-title {
      display: flex;
      justify-content: space-between;
      color: var(--text-muted);
      font-size: 8.5px;
    }

    .ramp-strip {
      width: 220px;
      height: 6px;
      border-radius: 1px;
      background: linear-gradient(to right,
        #04e9e7 0%,
        #019ff4 20%,
        #02fd02 40%,
        #ffff00 60%,
        #ff9f00 75%,
        #ff0000 88%,
        #d800ff 100%
      );
    }

    .ramp-ticks {
      display: flex;
      justify-content: space-between;
      color: var(--text-dim);
      font-size: 8px;
    }

    /* ==========================================================================
       BOTTOM: FORECAST TIMELINE CONTROL
       ========================================================================== */
    .bottom-timeline-deck {
      position: absolute;
      bottom: 14px;
      left: 20px;
      right: 20px;
      z-index: 1000;
      background: rgba(7, 11, 20, 0.94);
      backdrop-filter: blur(10px);
      border: 1px solid var(--border-line);
      border-radius: 3px;
      padding: 8px 14px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.8);
    }

    .timeline-top-meta {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .timeline-playback-bar {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .btn-play-action {
      background: var(--cyan-obs);
      border: none;
      width: 24px;
      height: 24px;
      border-radius: 2px;
      color: #000000;
      font-size: 11px;
      font-weight: bold;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .btn-play-action:hover { background: #7dd3fc; }

    .timeline-mode-label {
      font-family: var(--font-mono);
      font-size: 10.5px;
      font-weight: 600;
      color: var(--text-pure);
    }

    .timeline-horizon-strip {
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .horizon-pill {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 2px;
      padding: 3px 8px;
      font-family: var(--font-mono);
      font-size: 9.5px;
      color: var(--text-dim);
      cursor: pointer;
      transition: all 0.15s;
    }
    .horizon-pill:hover {
      color: var(--text-bright);
      border-color: var(--border-line);
    }
    .horizon-pill.active {
      background: rgba(56, 189, 248, 0.15);
      border-color: var(--cyan-obs);
      color: var(--cyan-obs);
      font-weight: 700;
    }

    .timeline-range-input {
      width: 100%;
      accent-color: var(--cyan-obs);
      cursor: pointer;
      height: 3px;
    }

    /* ==========================================================================
       RIGHT: CONTEXTUAL INTELLIGENCE PANEL (Operator's Intelligence Brief)
       ========================================================================== */
    .right-intel-panel {
      width: 330px;
      min-width: 330px;
      background: var(--bg-base);
      border-left: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      z-index: 500;
      overflow-y: auto;
    }

    .intel-cell-header {
      padding: 12px 14px;
      background: var(--bg-panel);
      border-bottom: 1px solid var(--border-subtle);
    }

    .cell-id-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .cell-id-title {
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 700;
      color: var(--text-pure);
      letter-spacing: 0.5px;
    }

    .cell-status-tag {
      font-family: var(--font-mono);
      font-size: 9px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 2px;
      background: rgba(239, 68, 68, 0.2);
      border: 1px solid rgba(239, 68, 68, 0.4);
      color: #fca5a5;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .cell-sub-callout {
      font-family: var(--font-mono);
      font-size: 10px;
      color: var(--red-severe);
      font-weight: 700;
      letter-spacing: 0.8px;
      margin-top: 3px;
    }

    /* Telemetry Table */
    .intel-data-table {
      width: 100%;
      border-collapse: collapse;
      font-family: var(--font-mono);
      font-size: 10px;
      margin-top: 8px;
    }

    .intel-data-table td {
      padding: 3px 0;
    }
    .intel-data-table td.k {
      color: var(--text-dim);
      width: 48%;
    }
    .intel-data-table td.v {
      color: var(--text-pure);
      font-weight: 600;
      text-align: right;
    }

    /* Section: THREAT */
    .intel-section {
      padding: 12px 14px;
      border-bottom: 1px solid var(--border-subtle);
    }

    .intel-section-title {
      font-family: var(--font-mono);
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.8px;
      color: var(--cyan-obs);
      text-transform: uppercase;
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .threat-metric-row {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .threat-bar-item {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .threat-bar-meta {
      display: flex;
      justify-content: space-between;
      font-family: var(--font-mono);
      font-size: 9.5px;
    }

    .bar-bg {
      height: 4px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 1px;
      overflow: hidden;
    }
    .bar-fill {
      height: 100%;
      border-radius: 1px;
    }

    /* Section: WHY NOW? (Evidence Signals) */
    .evidence-list {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .evidence-card {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 2px;
      padding: 6px 8px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-family: var(--font-mono);
      font-size: 10px;
    }

    .evidence-card .signal-name {
      display: flex;
      align-items: center;
      gap: 6px;
      color: var(--text-bright);
    }

    .evidence-card .signal-val {
      font-weight: 700;
      color: var(--red-severe);
    }

    /* Section: WHAT IS AT RISK? (Impact Infrastructure) */
    .risk-infra-list {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .risk-infra-item {
      background: var(--bg-panel);
      border-left: 2px solid var(--orange-elev);
      padding: 6px 8px;
      border-radius: 0 2px 2px 0;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .risk-infra-header {
      display: flex;
      justify-content: space-between;
      font-size: 10.5px;
      font-weight: 600;
      color: var(--text-pure);
    }

    .risk-infra-desc {
      font-size: 9.5px;
      color: var(--text-dim);
      line-height: 1.3;
    }

    /* Leaflet Overrides */
    .leaflet-container {
      background: #020408 !important;
    }

    /* Pulse Markers for Storm Centroid */
    .storm-core-marker {
      width: 22px;
      height: 22px;
      border-radius: 50%;
      background: rgba(239, 68, 68, 0.4);
      border: 2px solid #ef4444;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-family: var(--font-mono);
      font-size: 8.5px;
      font-weight: bold;
      box-shadow: 0 0 14px rgba(239, 68, 68, 0.8);
      cursor: pointer;
    }

    /* Lightning stroke marker */
    .lightning-strike-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--cyan-obs);
      box-shadow: 0 0 10px var(--cyan-obs);
      animation: lt-flash 1.4s infinite ease-out;
    }
    @keyframes lt-flash {
      0% { transform: scale(0.4); opacity: 1; }
      100% { transform: scale(3.2); opacity: 0; }
    }
  </style>
</head>
<body>

  <!-- ==========================================================================
       TOP: REFINED THIN STATUS / SYSTEM BAR
       ========================================================================== -->
  <header class="thin-status-bar">
    <div class="status-left-brand">
      <div class="brand-mark">
        VAJRA
        <span class="brand-tag">OPS-SPEC</span>
      </div>
      <span class="brand-subtitle">LIVE ATMOSPHERIC INTELLIGENCE</span>
    </div>

    <!-- Center System Telemetry -->
    <div class="status-telemetry-cluster">
      <div class="telemetry-item">
        <span class="telemetry-dot pulse"></span>
        <span class="telemetry-lbl">DATA FRESHNESS:</span>
        <span class="telemetry-val" id="telemetryFreshness">01m 24s</span>
      </div>

      <div class="telemetry-item">
        <span class="telemetry-lbl">MODEL:</span>
        <span class="telemetry-val">RF-ENSEMBLE v1.2</span>
      </div>

      <div class="telemetry-item">
        <span class="telemetry-lbl">LAST OBS:</span>
        <span class="telemetry-val" id="telemetryLastObs">13:15:00 UTC</span>
      </div>

      <div class="telemetry-item">
        <span class="telemetry-lbl">HORIZON:</span>
        <span class="telemetry-val" id="telemetryHorizon">NOW (T0) → T+120m</span>
      </div>

      <div class="telemetry-item">
        <span class="telemetry-lbl">SYSTEM HEALTH:</span>
        <span class="telemetry-val" style="color:var(--green-stable);">NOMINAL 99.98%</span>
      </div>
    </div>

    <!-- Right Clocks & Quick Controls -->
    <div class="status-right-tools">
      <div class="clock-ticker" id="systemClockZ">13:16:24Z</div>
      <button class="btn-status-pill" id="btnAudioToggle" title="Audio Warning Ping">
        <span>AUDIO: ON</span>
      </button>
      <button class="btn-status-pill" id="btnCapExport" title="Common Alerting Protocol Dispatch">
        <span>CAP ALERT</span>
      </button>
    </div>
  </header>

  <!-- ==========================================================================
       MAIN COMMAND WORKSPACE
       ========================================================================== */
  <main class="command-workspace">

    <!-- LEFT: COMPACT INTELLIGENCE / CONTROL RAIL -->
    <aside class="left-intel-rail">
      <!-- Active Threats Section -->
      <div class="rail-section">
        <div class="rail-section-header">
          <span>Active Threats</span>
          <span class="metric-badge" id="threatCountBadge">3 SEVERE CELLS</span>
        </div>
        <div class="threat-stat-grid">
          <div class="threat-stat-box">
            <span class="t-k">MAX INTENSITY</span>
            <span class="t-v severe" id="threatMaxDbz">64 dBZ</span>
          </div>
          <div class="threat-stat-box">
            <span class="t-k">LIGHTNING RATE</span>
            <span class="t-v elevated" id="threatLtgRate">82 /min</span>
          </div>
          <div class="threat-stat-box">
            <span class="t-k">SQUALL GUSTS</span>
            <span class="t-v severe">74 km/h</span>
          </div>
          <div class="threat-stat-box">
            <span class="t-k">ECHO TOPS</span>
            <span class="t-v">14.8 km</span>
          </div>
        </div>
      </div>

      <!-- Forecast Horizon Selector -->
      <div class="rail-section">
        <div class="rail-section-header">
          <span>Forecast Horizon</span>
          <span class="metric-badge" id="activeHorizonLabel">+30 MIN</span>
        </div>
        <select class="tactical-select" id="horizonDropdown">
          <option value="0">NOW (Observation T0)</option>
          <option value="15">+15 MIN (High Confidence)</option>
          <option value="30" selected>+30 MIN (Convective Peak)</option>
          <option value="45">+45 MIN (Impact Window)</option>
          <option value="60">+60 MIN (Advection Phase)</option>
          <option value="90">+90 MIN (Decay Corridor)</option>
          <option value="120">+120 MIN (Extended Watch)</option>
        </select>
      </div>

      <!-- Mission Scenario Selector -->
      <div class="rail-section">
        <div class="rail-section-header">
          <span>Atmospheric Domain</span>
        </div>
        <select class="tactical-select" id="scenarioSelect">
          <option value="scenario_bengal" selected>Bengal-Odisha (Nor'wester Supercell)</option>
          <option value="scenario_delhi">Delhi-NCR (Pre-Monsoon Squall)</option>
          <option value="scenario_telangana">Telangana (Severe Lightning Outbreak)</option>
          <option value="api">FastAPI Live Stream (Localhost:8000)</option>
        </select>
      </div>

      <!-- Atmospheric Layers Section -->
      <div class="rail-section" style="border-bottom:none; flex:1;">
        <div class="rail-section-header">
          <span>Atmospheric Layers</span>
          <span class="metric-badge">6 ACTIVE</span>
        </div>

        <div class="layer-toggle-group">
          <!-- Radar -->
          <div class="layer-row active" id="toggleRadar">
            <div class="layer-info">
              <span class="layer-indicator c-radar"></span>
              <div>
                <div class="layer-name">Radar Reflectivity</div>
                <div class="layer-sub">Composite dBZ (DWR Network)</div>
              </div>
            </div>
            <span class="layer-sub">ON</span>
          </div>

          <!-- Satellite -->
          <div class="layer-row active" id="toggleSat">
            <div class="layer-info">
              <span class="layer-indicator c-sat"></span>
              <div>
                <div class="layer-name">Satellite IR / WV</div>
                <div class="layer-sub">INSAT-3DR 10.8µm BT</div>
              </div>
            </div>
            <span class="layer-sub">ON</span>
          </div>

          <!-- Lightning -->
          <div class="layer-row active" id="toggleLtg">
            <div class="layer-info">
              <span class="layer-indicator c-ltg"></span>
              <div>
                <div class="layer-name">Lightning Activity</div>
                <div class="layer-sub">CG/IC Real-time Strokes</div>
              </div>
            </div>
            <span class="layer-sub">ON</span>
          </div>

          <!-- Storm Cells & Shadows -->
          <div class="layer-row active" id="toggleCells">
            <div class="layer-info">
              <span class="layer-indicator c-cell"></span>
              <div>
                <div class="layer-name">Storm Cells &amp; Shadows</div>
                <div class="layer-sub">Centroids + Future Shadows</div>
              </div>
            </div>
            <span class="layer-sub">ON</span>
          </div>

          <!-- Infrastructure -->
          <div class="layer-row active" id="toggleInfra">
            <div class="layer-info">
              <span class="layer-indicator c-infra"></span>
              <div>
                <div class="layer-name">Infrastructure Corridors</div>
                <div class="layer-sub">Airports, Power Grids, Rail</div>
              </div>
            </div>
            <span class="layer-sub">ON</span>
          </div>

          <!-- Population -->
          <div class="layer-row active" id="togglePop">
            <div class="layer-info">
              <span class="layer-indicator c-pop"></span>
              <div>
                <div class="layer-name">Population Risk</div>
                <div class="layer-sub">Settlement Exposure Gradients</div>
              </div>
            </div>
            <span class="layer-sub">ON</span>
          </div>
        </div>
      </div>
    </aside>

    <!-- CENTER HERO: THE MAP -->
    <section class="center-hero-map">
      <div id="vajraHeroMap"></div>

      <!-- Mode Selector: Observed vs AI Nowcast -->
      <div class="map-mode-toggle">
        <button class="mode-tab-btn" id="modeObserved">OBSERVED</button>
        <button class="mode-tab-btn active" id="modeNowcast">AI NOWCAST</button>
      </div>

      <!-- Radar dBZ Legend Overlay -->
      <div class="radar-ramp-bar">
        <div class="ramp-title">
          <span>RADAR REFLECTIVITY</span>
          <span style="color:var(--red-severe); font-weight:bold;">HAIL &gt; 55 dBZ</span>
        </div>
        <div class="ramp-strip"></div>
        <div class="ramp-ticks">
          <span>15</span>
          <span>25</span>
          <span>35</span>
          <span>45</span>
          <span>55</span>
          <span>65+ dBZ</span>
        </div>
      </div>

      <!-- BOTTOM: FORECAST TIMELINE -->
      <div class="bottom-timeline-deck">
        <div class="timeline-top-meta">
          <div class="timeline-playback-bar">
            <button class="btn-play-action" id="btnPlayPause">▶</button>
            <span class="timeline-mode-label" id="timelineModeLabel">AI NOWCAST (+30 MIN CONVECTIVE PEAK)</span>
          </div>

          <div class="timeline-horizon-strip">
            <button class="horizon-pill" data-idx="0">NOW</button>
            <button class="horizon-pill" data-idx="1">+15 MIN</button>
            <button class="horizon-pill active" data-idx="2">+30 MIN</button>
            <button class="horizon-pill" data-idx="3">+45 MIN</button>
            <button class="horizon-pill" data-idx="4">+60 MIN</button>
            <button class="horizon-pill" data-idx="5">+90 MIN</button>
            <button class="horizon-pill" data-idx="6">+120 MIN</button>
          </div>
        </div>

        <input type="range" class="timeline-range-input" id="timelineScrubber" min="0" max="6" value="2" step="1" />
      </div>
    </section>

    <!-- RIGHT: CONTEXTUAL INTELLIGENCE PANEL (Operator's Intelligence Brief) -->
    <aside class="right-intel-panel" id="rightIntelPanel">
      <!-- Storm Cell Header -->
      <div class="intel-cell-header">
        <div class="cell-id-row">
          <span class="cell-id-title" id="selectedCellId">STORM CELL #024</span>
          <span class="cell-status-tag" id="selectedCellStatus">CRITICAL WATCH</span>
        </div>
        <div class="cell-sub-callout" id="selectedCellCallout">RAPIDLY INTENSIFYING</div>

        <table class="intel-data-table">
          <tr>
            <td class="k">Location</td>
            <td class="v" id="cellCoord">22.42° N, 87.85° E (Midnapore)</td>
          </tr>
          <tr>
            <td class="k">Movement</td>
            <td class="v" id="cellMovement">ENE (068°) @ 46 km/h</td>
          </tr>
          <tr>
            <td class="k">Direction / Velocity</td>
            <td class="v" id="cellVelocity">Fast Squall Line</td>
          </tr>
          <tr>
            <td class="k">Current Intensity</td>
            <td class="v" style="color:var(--red-severe);" id="cellDbz">64.5 dBZ (Severe Hail)</td>
          </tr>
          <tr>
            <td class="k">Lightning Activity</td>
            <td class="v" style="color:var(--cyan-obs);" id="cellLtg">52 strokes/min (CG Dominant)</td>
          </tr>
          <tr>
            <td class="k">Confidence</td>
            <td class="v" style="color:var(--green-stable);">92.4% (Ensemble High)</td>
          </tr>
          <tr>
            <td class="k">Arrival Window</td>
            <td class="v" style="color:var(--orange-elev);" id="cellArrival">Kolkata Metro: 18-28 min</td>
          </tr>
        </table>
      </div>

      <!-- Section: THREAT -->
      <div class="intel-section">
        <div class="intel-section-title">
          <span>THREAT CLASSIFICATION</span>
          <span style="color:var(--red-severe);">LEVEL 4/4</span>
        </div>
        <div class="threat-metric-row">
          <div class="threat-bar-item">
            <div class="threat-bar-meta">
              <span>Severe Thunderstorm</span>
              <span style="color:var(--red-severe);">94% Probability</span>
            </div>
            <div class="bar-bg"><div class="bar-fill" style="width:94%; background:var(--red-severe);"></div></div>
          </div>
          <div class="threat-bar-item">
            <div class="threat-bar-meta">
              <span>Cloud-to-Ground Lightning</span>
              <span style="color:var(--cyan-obs);">88% High Density</span>
            </div>
            <div class="bar-bg"><div class="bar-fill" style="width:88%; background:var(--cyan-obs);"></div></div>
          </div>
          <div class="threat-bar-item">
            <div class="threat-bar-meta">
              <span>Heavy Precipitation &amp; Gusts</span>
              <span style="color:var(--orange-elev);">78 mm/h | 75 km/h</span>
            </div>
            <div class="bar-bg"><div class="bar-fill" style="width:82%; background:var(--orange-elev);"></div></div>
          </div>
        </div>
      </div>

      <!-- Section: WHY NOW? (Evidence Signals) -->
      <div class="intel-section">
        <div class="intel-section-title">
          <span>WHY NOW? (EVIDENCE SIGNALS)</span>
        </div>
        <div class="evidence-list">
          <div class="evidence-card">
            <span class="signal-name">Radar Growth Rate</span>
            <span class="signal-val">↑ +14 dBZ / 15m</span>
          </div>
          <div class="evidence-card">
            <span class="signal-name">Lightning Rate</span>
            <span class="signal-val">↑ +38 strikes/min</span>
          </div>
          <div class="evidence-card">
            <span class="signal-name">Cloud Development</span>
            <span class="signal-val">↑ Echo Top +2.4 km</span>
          </div>
          <div class="evidence-card">
            <span class="signal-name">Atmospheric Instability</span>
            <span class="signal-val">↑ SBCAPE 3,580 J/kg</span>
          </div>
        </div>
      </div>

      <!-- Section: WHAT IS AT RISK? (Impact Infrastructure) -->
      <div class="intel-section" style="border-bottom:none;">
        <div class="intel-section-title">
          <span>WHAT IS AT RISK?</span>
          <span style="color:var(--orange-elev);">EXPOSURE</span>
        </div>
        <div class="risk-infra-list">
          <div class="risk-infra-item">
            <div class="risk-infra-header">
              <span>✈ Airports</span>
              <span style="color:var(--red-severe);">VECC Kolkata</span>
            </div>
            <span class="risk-infra-desc">Ramp freeze advised. Microburst hazard across runway 19L/01R within 25 min.</span>
          </div>
          <div class="risk-infra-item">
            <div class="risk-infra-header">
              <span>⚡ Power Transmission</span>
              <span style="color:var(--orange-elev);">765kV Midnapore</span>
            </div>
            <span class="risk-infra-desc">Severe CG stroke rate. Substation trip vulnerability along Eastern Interconnect.</span>
          </div>
          <div class="risk-infra-item">
            <div class="risk-infra-header">
              <span>🛣 Major Highway Corridors</span>
              <span style="color:var(--orange-elev);">NH-16 &amp; NH-19</span>
            </div>
            <span class="risk-infra-desc">Extreme crosswinds &gt; 70 km/h and localized visibility &lt; 200m.</span>
          </div>
          <div class="risk-infra-item">
            <div class="risk-infra-header">
              <span>👥 Population Settlements</span>
              <span style="color:var(--red-severe);">2.4M Persons</span>
            </div>
            <span class="risk-infra-desc">High-density urban wards exposed in Howrah, Kolkata, and Hooghly.</span>
          </div>
        </div>
      </div>
    </aside>
  </main>

  <!-- ==========================================================================
       JAVASCRIPT: MISSION LOGIC & SCIENTIFIC RENDERING ENGINE
       ========================================================================== -->
  <script>
    /* ==========================================================================
       1. DATASETS & SCENARIO ENGINE
       ========================================================================== */
    const MISSION_DATA = {
      scenario_bengal: {
        center: [22.65, 88.25],
        zoom: 8,
        activeThreats: "3 SEVERE CELLS",
        maxDbz: "64.5 dBZ",
        ltgRate: "82 /min",
        cells: [
          {
            id: "STORM CELL #024",
            name: "Midnapore-Howrah Core",
            status: "CRITICAL WATCH",
            callout: "RAPIDLY INTENSIFYING",
            lat: 22.42,
            lon: 87.85,
            movement: "ENE (068°) @ 46 km/h",
            velocity: "Fast Squall Line",
            dbz: 64.5,
            vil: 67.2,
            echoTop: 15.2,
            ltg: "52 strokes/min (CG Dominant)",
            confidence: "92.4% (Ensemble High)",
            arrival: "Kolkata Metro: 18-28 min",
            // Trajectory waypoints: [T0, +15m, +30m, +45m, +60m, +90m, +120m]
            track: [
              [22.42, 87.85],
              [22.51, 88.08],
              [22.60, 88.32],
              [22.68, 88.54],
              [22.76, 88.76],
              [22.88, 89.10],
              [23.00, 89.45]
            ],
            // Uncertainty cone expansion factors
            coneExpansion: [0.08, 0.14, 0.22, 0.32, 0.44, 0.60, 0.78]
          },
          {
            id: "STORM CELL #019",
            name: "Burdwan Convective Cluster",
            status: "ELEVATED",
            callout: "STEADY INTENSITY",
            lat: 23.24,
            lon: 87.88,
            movement: "ENE (075°) @ 38 km/h",
            velocity: "Organized Multi-cell",
            dbz: 56.2,
            vil: 48.0,
            echoTop: 13.4,
            ltg: "22 strokes/min",
            confidence: "88.1%",
            arrival: "Ranaghat: 35 min",
            track: [
              [23.24, 87.88],
              [23.29, 88.12],
              [23.34, 88.36],
              [23.39, 88.60],
              [23.44, 88.84],
              [23.52, 89.15],
              [23.60, 89.46]
            ],
            coneExpansion: [0.06, 0.12, 0.18, 0.26, 0.36, 0.50, 0.65]
          },
          {
            id: "STORM CELL #031",
            name: "Balasore Coastal Squall",
            status: "SEVERE",
            callout: "COASTAL CONVERGENCE",
            lat: 21.65,
            lon: 87.05,
            movement: "NE (055°) @ 52 km/h",
            velocity: "Bow Echo Segment",
            dbz: 58.8,
            vil: 52.4,
            echoTop: 14.1,
            ltg: "38 strokes/min",
            confidence: "90.5%",
            arrival: "Digha: 16 min",
            track: [
              [21.65, 87.05],
              [21.80, 87.28],
              [21.95, 87.52],
              [22.10, 87.76],
              [22.25, 88.00],
              [22.45, 88.35],
              [22.65, 88.70]
            ],
            coneExpansion: [0.07, 0.13, 0.20, 0.28, 0.38, 0.52, 0.68]
          }
        ],
        lightnings: [
          [22.44, 87.87], [22.41, 87.82], [22.47, 87.92],
          [23.22, 87.85], [23.26, 87.91],
          [21.67, 87.08], [21.62, 87.03]
        ]
      },
      scenario_delhi: {
        center: [28.60, 77.15],
        zoom: 8,
        activeThreats: "2 SEVERE CELLS",
        maxDbz: "61.2 dBZ",
        ltgRate: "64 /min",
        cells: [
          {
            id: "STORM CELL #008",
            name: "Gurugram-Dwarka Frontal Core",
            status: "CRITICAL WATCH",
            callout: "RAPIDLY INTENSIFYING",
            lat: 28.38,
            lon: 76.92,
            movement: "ENE (065°) @ 55 km/h",
            velocity: "Severe Squall Line",
            dbz: 61.2,
            vil: 58.4,
            echoTop: 14.5,
            ltg: "44 strokes/min",
            confidence: "94.2%",
            arrival: "IGI Airport: 12 min",
            track: [
              [28.38, 76.92],
              [28.48, 77.14],
              [28.58, 77.36],
              [28.68, 77.58],
              [28.78, 77.80],
              [28.92, 78.10],
              [29.05, 78.40]
            ],
            coneExpansion: [0.08, 0.15, 0.24, 0.34, 0.46, 0.62, 0.80]
          }
        ],
        lightnings: [
          [28.39, 76.94], [28.42, 76.98], [28.36, 76.90]
        ]
      },
      scenario_telangana: {
        center: [17.40, 78.50],
        zoom: 8,
        activeThreats: "1 INTENSE CELL",
        maxDbz: "59.8 dBZ",
        ltgRate: "72 /min",
        cells: [
          {
            id: "STORM CELL #012",
            name: "Secunderabad North Core",
            status: "SEVERE",
            callout: "PULSE CONVECTION",
            lat: 17.52,
            lon: 78.48,
            movement: "ESE (110°) @ 34 km/h",
            velocity: "Slow-moving Cluster",
            dbz: 59.8,
            vil: 54.0,
            echoTop: 14.2,
            ltg: "62 strokes/min",
            confidence: "89.6%",
            arrival: "Begumpet: 15 min",
            track: [
              [17.52, 78.48],
              [17.47, 78.64],
              [17.42, 78.80],
              [17.37, 78.96],
              [17.32, 79.12],
              [17.25, 79.35],
              [17.18, 79.58]
            ],
            coneExpansion: [0.06, 0.12, 0.20, 0.28, 0.38, 0.50, 0.65]
          }
        ],
        lightnings: [
          [17.53, 78.49], [17.50, 78.46], [17.48, 78.52]
        ]
      }
    };

    let activeScenario = MISSION_DATA.scenario_bengal;
    let selectedCell = activeScenario.cells[0];
    let map = null;

    // Map layer containers
    let layerRadar = null;
    let layerSat = null;
    let layerLtg = null;
    let layerCells = null;
    let layerInfra = null;
    let layerPop = null;

    let currentHorizonIndex = 2; // Default +30 min
    let currentMode = "nowcast"; // "observed" or "nowcast"
    let isPlaying = false;
    let playbackTimer = null;
    let audioPingEnabled = true;

    /* ==========================================================================
       2. INITIALIZATION
       ========================================================================== */
    window.addEventListener("DOMContentLoaded", () => {
      initSystemClocks();
      initHeroMap();
      setupEventListeners();
      loadMissionScenario(activeScenario);
    });

    /* ==========================================================================
       3. SYSTEM CLOCKS
       ========================================================================== */
    function initSystemClocks() {
      const zuluClock = document.getElementById("systemClockZ");
      function tick() {
        const d = new Date();
        const h = String(d.getUTCHours()).padStart(2, '0');
        const m = String(d.getUTCMinutes()).padStart(2, '0');
        const s = String(d.getUTCSeconds()).padStart(2, '0');
        zuluClock.textContent = `${h}:${m}:${s}Z`;
      }
      setInterval(tick, 1000);
      tick();
    }

    /* ==========================================================================
       4. HERO MAP INITIALIZATION
       ========================================================================== */
    function initHeroMap() {
      map = L.map("vajraHeroMap", {
        zoomControl: false,
        attributionControl: false,
        preferCanvas: true
      }).setView(activeScenario.center, activeScenario.zoom);

      L.control.zoom({ position: 'topright' }).addTo(map);

      // Dark Matter Carto Tactical Basemap
      L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 18,
        subdomains: 'abcd',
        opacity: 0.94
      }).addTo(map);

      // Layer groups
      layerRadar = L.layerGroup().addTo(map);
      layerSat = L.layerGroup().addTo(map);
      layerLtg = L.layerGroup().addTo(map);
      layerCells = L.layerGroup().addTo(map);
      layerInfra = L.layerGroup().addTo(map);
      layerPop = L.layerGroup().addTo(map);
    }

    /* ==========================================================================
       5. SCIENTIFIC VISUALIZATION: STORM SHADOW & UNCERTAINTY CORRIDOR
       ========================================================================== */
    function renderMapIntelligence() {
      layerRadar.clearLayers();
      layerLtg.clearLayers();
      layerCells.clearLayers();
      layerInfra.clearLayers();
      layerPop.clearLayers();

      const horizonSteps = [0, 15, 30, 45, 60, 90, 120];
      const hIdx = currentHorizonIndex;

      activeScenario.cells.forEach(cell => {
        const isSelected = (cell.id === selectedCell.id);

        // 1. STORM CELL TRACK (Clean trajectory line)
        if (cell.track && cell.track.length > 1) {
          L.polyline(cell.track, {
            color: '#38bdf8',
            weight: 2,
            opacity: 0.85,
            dashArray: '4, 4'
          }).addTo(layerCells);
        }

        // 2. UNCERTAINTY CORRIDOR (Expanding cone of probability with time)
        if (cell.track && currentMode === "nowcast") {
          const pStart = cell.track[0];
          const targetPt = cell.track[hIdx] || cell.track[cell.track.length - 1];
          const spread = cell.coneExpansion[hIdx] || 0.25;

          const corridorPolygon = [
            [pStart[0], pStart[1]],
            [targetPt[0] + spread * 0.7, targetPt[1] - spread],
            [targetPt[0] + spread, targetPt[1] + spread],
            [targetPt[0] - spread * 0.5, targetPt[1] + spread * 0.8],
            [pStart[0], pStart[1]]
          ];

          L.polygon(corridorPolygon, {
            color: '#c084fc',
            fillColor: '#c084fc',
            fillOpacity: 0.12,
            weight: 1,
            dashArray: '3, 4'
          }).addTo(layerCells);
        }

        // 3. CURRENT STORM (Shown strongly at T0)
        const t0Pt = cell.track[0];
        L.circle(t0Pt, {
          radius: 18000,
          color: '#ef4444',
          fillColor: '#ef4444',
          fillOpacity: 0.5,
          weight: 1.5
        }).addTo(layerRadar);

        L.circle(t0Pt, {
          radius: 8000,
          color: '#d946ef',
          fillColor: '#ffffff',
          fillOpacity: 0.75,
          weight: 2
        }).addTo(layerRadar);

        // 4. STORM SHADOWS (Progressively translucent future positions!)
        if (currentMode === "nowcast") {
          for (let step = 1; step <= hIdx; step++) {
            const shadowPt = cell.track[step];
            if (!shadowPt) continue;

            // Translucency decays as forecast horizon expands
            const opacity = Math.max(0.12, 0.45 - (step * 0.06));
            const shadowRadius = 18000 + (step * 2500);

            L.circle(shadowPt, {
              radius: shadowRadius,
              color: '#f97316',
              fillColor: '#f97316',
              fillOpacity: opacity,
              weight: 1,
              dashArray: '4, 4'
            }).addTo(layerRadar);

            // Waypoint Dot
            L.circleMarker(shadowPt, {
              radius: 4,
              color: '#38bdf8',
              fillColor: '#070b14',
              fillOpacity: 1,
              weight: 2
            }).bindTooltip(`+${horizonSteps[step]}m (${cell.id})`, {
              permanent: false
            }).addTo(layerCells);
          }
        }

        // 5. Centroid Marker
        const activePt = (currentMode === "nowcast" && hIdx > 0) ? cell.track[hIdx] : t0Pt;
        const icon = L.divIcon({
          className: 'storm-marker-wrap',
          html: `<div class="storm-core-marker" title="${cell.name}">${Math.round(cell.dbz)}</div>`,
          iconSize: [22, 22],
          iconAnchor: [11, 11]
        });

        const marker = L.marker(activePt, { icon: icon }).addTo(layerCells);
        marker.on('click', () => {
          selectStormCell(cell);
        });
      });

      // 6. LIGHTNING ACTIVITY (Strobe pulses communicating temporal density)
      activeScenario.lightnings.forEach(ltg => {
        const icon = L.divIcon({
          className: 'ltg-marker-wrap',
          html: '<div class="lightning-strike-dot"></div>',
          iconSize: [10, 10],
          iconAnchor: [5, 5]
        });
        L.marker(ltg, { icon: icon }).addTo(layerLtg);
      });

      // 7. CRITICAL INFRASTRUCTURE (Airports, Power Stations)
      const infraPoints = [
        { code: "VECC", name: "Kolkata Airport", pt: [22.654, 88.446], alert: true },
        { code: "VIDP", name: "Delhi IGI", pt: [28.556, 77.100], alert: false },
        { code: "GRID-MID", name: "765kV Substation", pt: [22.40, 87.32], alert: true }
      ];

      infraPoints.forEach(inf => {
        L.circleMarker(inf.pt, {
          radius: 5,
          color: inf.alert ? '#ef4444' : '#e2e8f0',
          fillColor: inf.alert ? '#ef4444' : '#070b14',
          fillOpacity: 0.9,
          weight: 2
        }).bindTooltip(`${inf.code}: ${inf.name} [${inf.alert ? 'CRITICAL RISK' : 'NORMAL'}]`, {
          permanent: false
        }).addTo(layerInfra);
      });
    }

    /* ==========================================================================
       6. CONTEXTUAL INTELLIGENCE SELECTION (Right Panel Update)
       ========================================================================== */
    function selectStormCell(cell) {
      selectedCell = cell;

      document.getElementById("selectedCellId").textContent = cell.id;
      document.getElementById("selectedCellStatus").textContent = cell.status;
      document.getElementById("selectedCellCallout").textContent = cell.callout;
      document.getElementById("cellCoord").textContent = `${cell.lat.toFixed(2)}° N, ${cell.lon.toFixed(2)}° E`;
      document.getElementById("cellMovement").textContent = cell.movement;
      document.getElementById("cellVelocity").textContent = cell.velocity;
      document.getElementById("cellDbz").textContent = `${cell.dbz} dBZ`;
      document.getElementById("cellLtg").textContent = cell.ltg;
      document.getElementById("cellArrival").textContent = cell.arrival;

      renderMapIntelligence();

      if (audioPingEnabled && cell.status.includes("CRITICAL")) {
        triggerAudioPing();
      }
    }

    /* ==========================================================================
       7. AUDIO ALERT PING (Web Audio API Synthesizer)
       ========================================================================== */
    function triggerAudioPing() {
      try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        const ctx = new AudioCtx();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.type = "triangle";
        osc.frequency.setValueAtTime(880, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(440, ctx.currentTime + 0.2);

        gain.gain.setValueAtTime(0.12, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.2);

        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.2);
      } catch (e) {}
    }

    /* ==========================================================================
       8. TIMELINE & HORIZON CONTROLLER
       ========================================================================== */
    function setHorizon(idx) {
      currentHorizonIndex = idx;
      document.getElementById("timelineScrubber").value = idx;

      const pills = document.querySelectorAll(".horizon-pill");
      pills.forEach((p, i) => p.classList.toggle("active", i === idx));

      const labels = [
        "OBSERVATION (T0 CURRENT)",
        "AI NOWCAST (+15 MIN HIGH CONFIDENCE)",
        "AI NOWCAST (+30 MIN CONVECTIVE PEAK)",
        "AI NOWCAST (+45 MIN IMPACT WINDOW)",
        "AI NOWCAST (+60 MIN ADVECTION PHASE)",
        "AI EXTENDED (+90 MIN DECAY CORRIDOR)",
        "AI EXTENDED (+120 MIN WATCH)"
      ];
      document.getElementById("timelineModeLabel").textContent = labels[idx];

      const horizonValues = ["NOW (T0)", "+15 MIN", "+30 MIN", "+45 MIN", "+60 MIN", "+90 MIN", "+120 MIN"];
      document.getElementById("activeHorizonLabel").textContent = horizonValues[idx];
      document.getElementById("telemetryHorizon").textContent = `NOW (T0) → ${horizonValues[idx]}`;

      renderMapIntelligence();
    }

    /* ==========================================================================
       9. MISSION SCENARIO LOADER
       ========================================================================== */
    function loadMissionScenario(sc) {
      activeScenario = sc;
      selectedCell = sc.cells[0];
      map.flyTo(sc.center, sc.zoom, { duration: 1.0 });

      document.getElementById("threatCountBadge").textContent = sc.activeThreats;
      document.getElementById("threatMaxDbz").textContent = sc.maxDbz;
      document.getElementById("threatLtgRate").textContent = sc.ltgRate;

      selectStormCell(selectedCell);
    }

    /* ==========================================================================
       10. EVENT HANDLERS
       ========================================================================== */
    function setupEventListeners() {
      // Horizon Pills
      document.querySelectorAll(".horizon-pill").forEach(pill => {
        pill.addEventListener("click", () => {
          setHorizon(parseInt(pill.dataset.idx));
        });
      });

      // Range Scrubber
      document.getElementById("timelineScrubber").addEventListener("input", (e) => {
        setHorizon(parseInt(e.target.value));
      });

      // Horizon Dropdown in Rail
      document.getElementById("horizonDropdown").addEventListener("change", (e) => {
        const val = parseInt(e.target.value);
        const mapSteps = { 0: 0, 15: 1, 30: 2, 45: 3, 60: 4, 90: 5, 120: 6 };
        setHorizon(mapSteps[val] || 0);
      });

      // Playback Play / Pause
      const playBtn = document.getElementById("btnPlayPause");
      playBtn.addEventListener("click", () => {
        isPlaying = !isPlaying;
        playBtn.textContent = isPlaying ? "⏸" : "▶";
        if (isPlaying) {
          playbackTimer = setInterval(() => {
            let next = (currentHorizonIndex + 1) % 7;
            setHorizon(next);
          }, 1600);
        } else {
          clearInterval(playbackTimer);
        }
      });

      // Observed vs AI Nowcast Modes
      document.getElementById("modeObserved").addEventListener("click", () => {
        currentMode = "observed";
        document.getElementById("modeObserved").classList.add("active");
        document.getElementById("modeNowcast").classList.remove("active");
        renderMapIntelligence();
      });

      document.getElementById("modeNowcast").addEventListener("click", () => {
        currentMode = "nowcast";
        document.getElementById("modeNowcast").classList.add("active");
        document.getElementById("modeObserved").classList.remove("active");
        renderMapIntelligence();
      });

      // Scenario Picker
      document.getElementById("scenarioSelect").addEventListener("change", (e) => {
        const val = e.target.value;
        if (MISSION_DATA[val]) {
          loadMissionScenario(MISSION_DATA[val]);
        }
      });

      // Layer Toggles
      const setupLayerToggle = (elemId, layerObj) => {
        const el = document.getElementById(elemId);
        el.addEventListener("click", () => {
          el.classList.toggle("active");
          const isOn = el.classList.contains("active");
          el.querySelector(".layer-sub").textContent = isOn ? "ON" : "OFF";
          if (isOn) map.addLayer(layerObj);
          else map.removeLayer(layerObj);
        });
      };

      setupLayerToggle("toggleRadar", layerRadar);
      setupLayerToggle("toggleSat", layerSat);
      setupLayerToggle("toggleLtg", layerLtg);
      setupLayerToggle("toggleCells", layerCells);
      setupLayerToggle("toggleInfra", layerInfra);
      setupLayerToggle("togglePop", layerPop);

      // Audio Ping Toggle
      const audioBtn = document.getElementById("btnAudioToggle");
      audioBtn.addEventListener("click", () => {
        audioPingEnabled = !audioPingEnabled;
        audioBtn.textContent = audioPingEnabled ? "AUDIO: ON" : "AUDIO: MUTE";
        audioBtn.classList.toggle("active", audioPingEnabled);
      });

      // CAP Alert export
      document.getElementById("btnCapExport").addEventListener("click", () => {
        const alertText = `NATIONAL DISASTER ADVISORY (VAJRA NOWCAST)\\nTHREAT: ${selectedCell.id} - ${selectedCell.callout}\\nCOORDINATES: ${selectedCell.lat}N, ${selectedCell.lon}E\\nRADAR INTENSITY: ${selectedCell.dbz} dBZ\\nIMPACT CORRIDOR: ${selectedCell.arrival}\\nADVISORY: Immediate shelter recommended for civil population; aerodromes ground hold.`;
        navigator.clipboard.writeText(alertText);
        alert("CAP Alert advisory copied to clipboard!");
      });
    }
  </script>
</body>
</html>
"""

with open("dashboard/index.html", "w", encoding="utf-8") as f:
    f.write(html_code)

print(f"Generated precision VAJRA dashboard: {len(html_code)} bytes")
